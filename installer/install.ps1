# S&M — Security & Maintenance Toolkit
# Main Installer GUI

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Import shared functions
. "$PSScriptRoot\functions.ps1"

$tools = Load-Tools

# -----------------------------
# GUI — Main Window
# -----------------------------
$form = New-Object System.Windows.Forms.Form
$form.Text = "S&M Security & Maintenance — Setup Wizard"
$form.Size = New-Object System.Drawing.Size(600, 500)
$form.StartPosition = "CenterScreen"

# Title
$title = New-Object System.Windows.Forms.Label
$title.Text = "Welcome to S&M Security & Maintenance Toolkit"
$title.AutoSize = $true
$title.Font = "Segoe UI,14,style=Bold"
$title.Location = "20,20"
$form.Controls.Add($title)

# Checkbox list
$list = New-Object System.Windows.Forms.CheckedListBox
$list.Location = "20,80"
$list.Size = "540,300"
foreach ($t in $tools) {
    $list.Items.Add($t.name)
}
$form.Controls.Add($list)

# Install button
$installBtn = New-Object System.Windows.Forms.Button
$installBtn.Text = "Install Selected"
$installBtn.Location = "20,400"
$installBtn.Size = "150,30"
$form.Controls.Add($installBtn)

# Progress bar
$progress = New-Object System.Windows.Forms.ProgressBar
$progress.Location = "200,400"
$progress.Size = "360,30"
$form.Controls.Add($progress)

# Button click event
$installBtn.Add_Click({
    $selected = @()
    foreach ($i in $list.CheckedItems) {
        $selected += $tools | Where-Object { $_.name -eq $i }
    }

    $count = $selected.Count
    $step = 100 / $count
    $progress.Value = 0

    foreach ($tool in $selected) {
        Write-Log "Installing $($tool.name)"
        Install-Tool $tool
        $progress.Value += $step
    }

    [System.Windows.Forms.MessageBox]::Show("All selected tools have been installed.", "S&M")
})

$form.ShowDialog()
