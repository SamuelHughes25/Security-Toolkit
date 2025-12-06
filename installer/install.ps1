# S&M Security & Maintenance Toolkit - Upgraded Installer
# Multi-step Setup Wizard
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Import shared functions
. "$PSScriptRoot\functions.ps1"

$tools = Load-Tools

# -----------------------------
# Create Main Form
# -----------------------------
$form = New-Object System.Windows.Forms.Form
$form.Text = "S&M Security & Maintenance Toolkit Setup"
$form.Size = New-Object System.Drawing.Size(600, 450)
$form.StartPosition = "CenterScreen"
$form.FormBorderStyle = 'FixedDialog'
$form.MaximizeBox = $false
$form.MinimizeBox = $false

# -----------------------------
# Panels for Wizard Steps
# -----------------------------
$panelWelcome = New-Object System.Windows.Forms.Panel
$panelWelcome.Dock = 'Fill'
$form.Controls.Add($panelWelcome)

$panelSelectTools = New-Object System.Windows.Forms.Panel
$panelSelectTools.Dock = 'Fill'
$panelSelectTools.Visible = $false
$form.Controls.Add($panelSelectTools)

$panelProgress = New-Object System.Windows.Forms.Panel
$panelProgress.Dock = 'Fill'
$panelProgress.Visible = $false
$form.Controls.Add($panelProgress)

$panelFinish = New-Object System.Windows.Forms.Panel
$panelFinish.Dock = 'Fill'
$panelFinish.Visible = $false
$form.Controls.Add($panelFinish)

# -----------------------------
# Welcome Panel
# -----------------------------
$lblWelcome = New-Object System.Windows.Forms.Label
$lblWelcome.Text = "Welcome to S&M Security & Maintenance Toolkit"
$lblWelcome.Font = 'Segoe UI,14,style=Bold'
$lblWelcome.AutoSize = $true
$lblWelcome.Location = '20,20'
$panelWelcome.Controls.Add($lblWelcome)

$lblDesc = New-Object System.Windows.Forms.Label
$lblDesc.Text = "This setup will help you install essential tools and optionally harden your system."
$lblDesc.AutoSize = $true
$lblDesc.Location = '20,60'
$panelWelcome.Controls.Add($lblDesc)

$btnNextWelcome = New-Object System.Windows.Forms.Button
$btnNextWelcome.Text = "Next >"
$btnNextWelcome.Size = '100,30'
$btnNextWelcome.Location = '460,360'
$panelWelcome.Controls.Add($btnNextWelcome)

$btnNextWelcome.Add_Click({
    $panelWelcome.Visible = $false
    $panelSelectTools.Visible = $true
})

# -----------------------------
# Tool Selection Panel
# -----------------------------
$lblSelect = New-Object System.Windows.Forms.Label
$lblSelect.Text = "Select tools to install:"
$lblSelect.Font = 'Segoe UI,12,style=Bold'
$lblSelect.AutoSize = $true
$lblSelect.Location = '20,20'
$panelSelectTools.Controls.Add($lblSelect)

# CheckedListBox
$chkTools = New-Object System.Windows.Forms.CheckedListBox
$chkTools.Location = '20,60'
$chkTools.Size = '540,250'
foreach ($t in $tools) {
    $chkTools.Items.Add($t.name)
}
$panelSelectTools.Controls.Add($chkTools)

# Optional tool description label
$lblToolDesc = New-Object System.Windows.Forms.Label
$lblToolDesc.Text = ""
$lblToolDesc.AutoSize = $true
$lblToolDesc.Location = '20,320'
$panelSelectTools.Controls.Add($lblToolDesc)

$chkTools.Add_SelectedIndexChanged({
    $index = $chkTools.SelectedIndex
    if ($index -ge 0) {
        $tool = $tools[$index]
        $lblToolDesc.Text = if ($tool.description) { $tool.description } else { "No description available" }
    }
})

# Navigation buttons
$btnBackSelect = New-Object System.Windows.Forms.Button
$btnBackSelect.Text = "< Back"
$btnBackSelect.Size = '100,30'
$btnBackSelect.Location = '20,360'
$panelSelectTools.Controls.Add($btnBackSelect)

$btnNextSelect = New-Object System.Windows.Forms.Button
$btnNextSelect.Text = "Install >"
$btnNextSelect.Size = '100,30'
$btnNextSelect.Location = '460,360'
$panelSelectTools.Controls.Add($btnNextSelect)

$btnBackSelect.Add_Click({
    $panelSelectTools.Visible = $false
    $panelWelcome.Visible = $true
})

$btnNextSelect.Add_Click({
    $selected = @()
    foreach ($i in $chkTools.CheckedItems) {
        $selected += $tools | Where-Object { $_.name -eq $i }
    }

    if ($selected.Count -eq 0) {
        [System.Windows.Forms.MessageBox]::Show("Please select at least one tool to continue.","S&M")
        return
    }

    $panelSelectTools.Visible = $false
    $panelProgress.Visible = $true

    # Run installation in background to update progress
    $progressBar.Value = 0
    $step = 100 / $selected.Count
    foreach ($tool in $selected) {
        Write-Log "Installing $($tool.name)"
        Install-Tool $tool
        $progressBar.Value += $step
        $lblProgress.Text = "Installing $($tool.name)..."
        $form.Refresh()
    }

    $panelProgress.Visible = $false
    $panelFinish.Visible = $true
})

# -----------------------------
# Progress Panel
# -----------------------------
$lblProgress = New-Object System.Windows.Forms.Label
$lblProgress.Text = "Installing tools..."
$lblProgress.AutoSize = $true
$lblProgress.Location = '20,20'
$panelProgress.Controls.Add($lblProgress)

$progressBar = New-Object System.Windows.Forms.ProgressBar
$progressBar.Location = '20,60'
$progressBar.Size = '540,30'
$panelProgress.Controls.Add($progressBar)

# -----------------------------
# Finish Panel
# -----------------------------
$lblFinish = New-Object System.Windows.Forms.Label
$lblFinish.Text = "Installation Complete!"
$lblFinish.Font = 'Segoe UI,14,style=Bold'
$lblFinish.AutoSize = $true
$lblFinish.Location = '20,20'
$panelFinish.Controls.Add($lblFinish)

$lblFinishDesc = New-Object System.Windows.Forms.Label
$lblFinishDesc.Text = "All selected tools have been installed. Logs are saved in %TEMP%\SM-Toolkit.log"
$lblFinishDesc.AutoSize = $true
$lblFinishDesc.Location = '20,60'
$panelFinish.Controls.Add($lblFinishDesc)

$btnFinish = New-Object System.Windows.Forms.Button
$btnFinish.Text = "Finish"
$btnFinish.Size = '100,30'
$btnFinish.Location = '460,360'
$panelFinish.Controls.Add($btnFinish)

$btnFinish.Add_Click({
    $form.Close()
})

# -----------------------------
# Show Form
# -----------------------------
$form.ShowDialog()
