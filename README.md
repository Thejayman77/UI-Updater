# UI-Updater
This little helper utility can monitor a work-in-progress .UI file being created in QT designer.

Once the file is selected, it will be immediately converted to its importable .py format.  From there, you can enable the interval timer to monitor it every <interval> # of seconds for changes, or select the one-time button to convert as needed.

The status button will turn green while the monitoring is running, and will be dark gray otherwise.

It's the first version.  For now, it's basic, but does the trick so you don't have to run any pyuic5 commands manually.

