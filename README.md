# Cheetah Template Beautifier

A Python script that reformats Cheetah templates to improve readability by adjusting indentation for HTML, Cheetah directives, and embedded JavaScript code.

## Features

- **Smart Indentation:** Automatically adjusts indentation for HTML tags, Cheetah directives (`#if`, `#for`, `#def`, `#else`, `#elif`, `#end`), and JavaScript blocks
- **Multiple File Types:** Supports both `.tmpl` and `.inc` file extensions
- **Void Element Handling:** Correctly handles HTML void elements (e.g., `<br>`, `<img>`, `<input>`) that don't have closing tags
- **Self-Closing Tags:** Properly handles self-closing XML/XHTML tags
- **Recursive Processing:** Can recursively find and reformat all template files in a directory tree
- **JavaScript Support:** Formats JavaScript code blocks with proper brace and bracket indentation
- **Multiline Tag Support:** Handles HTML tags that span multiple lines
- **Blank Line Cleanup:** Removes excessive consecutive blank lines while preserving intentional spacing
- **In-place or Output File:** Reformat files in-place or write output to new files

## Installation

No installation required. Just download the script and run it with Python 3.

```bash
# Download the script
wget https://raw.githubusercontent.com/seehase/cheetah_template_beautifier/main/cheetah_template_beautifier.py

# Make it executable (optional)
chmod +x cheetah_template_beautifier.py
```

## Usage

### Basic Usage

```bash
# Format a single file in-place
python cheetah_template_beautifier.py template.tmpl

# Format a single .inc file
python cheetah_template_beautifier.py include.inc

# Format and save to a different location
python cheetah_template_beautifier.py template.tmpl -o formatted_template.tmpl
```

### Recursive Processing

```bash
# Recursively format all .tmpl and .inc files in a directory
python cheetah_template_beautifier.py -r /path/to/templates/

# Process current directory recursively
python cheetah_template_beautifier.py -r .
```

### Help and Version

```bash
# Show help
python cheetah_template_beautifier.py -h

# Show version
python cheetah_template_beautifier.py --version
```

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
python -m unittest test_cheetah_template_beautifier.py

# Run tests with verbose output
python -m unittest test_cheetah_template_beautifier.py -v

# Run a specific test
python -m unittest test_cheetah_template_beautifier.TestCheetahTemplateBeautifier.test_html_indentation
```

## Examples

### Basic HTML Formatting

**Before:**
```html
<div>
<p>Hello World</p>
<ul>
<li>Item 1</li>
<li>Item 2</li>
</ul>
</div>
```

**After:**
```html
<div>
    <p>Hello World</p>
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
    </ul>
</div>
```

### Cheetah Directives

**Before:**
```cheetah
#if $user
<div>
<p>Hello $user.name</p>
#if $user.admin
<span>Admin User</span>
#end if
</div>
#else
<p>Not logged in</p>
#end if
```

**After:**
```cheetah
#if $user
    <div>
        <p>Hello $user.name</p>
        #if $user.admin
            <span>Admin User</span>
        #end if
    </div>
#else
    <p>Not logged in</p>
#end if
```

### JavaScript Code

**Before:**
```javascript
function initPage() {
var config = {
api: 'http://example.com',
headers: [
'Content-Type: application/json'
]
};
if (config.api) {
loadData(config);
}
}
```

**After:**
```javascript
function initPage() {
    var config = {
        api: 'http://example.com',
        headers: [
            'Content-Type: application/json'
        ]
    };
    if (config.api) {
        loadData(config);
    }
}
```

### Mixed Cheetah and HTML

**Before:**
```cheetah
#for $item in $items
<div class="item">
#if $item.featured
<span class="badge">Featured</span>
#end if
<h3>$item.title</h3>
<p>$item.description</p>
</div>
#end for
```

**After:**
```cheetah
#for $item in $items
    <div class="item">
        #if $item.featured
            <span class="badge">Featured</span>
        #end if
        <h3>$item.title</h3>
        <p>$item.description</p>
    </div>
#end for
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `source` | The path to the source file or directory |
| `-o, --outfile` | The path to the output file (not valid with --recursive) |
| `-r, --recursive` | Recursively find and reformat all *.tmpl and *.inc files |
| `--version` | Show program's version number and exit |
| `-h, --help` | Show help message and exit |

## Supported File Extensions

- `.tmpl` - Cheetah template files
- `.inc` - Include files (often used for Cheetah templates)

## Error Handling

The script provides clear error messages for common issues:

- **File not found:** Clear message when source file doesn't exist
- **Invalid directory:** Error when using `-r` with a non-existent directory
- **Permission errors:** Helpful message when unable to write output files
- **Invalid arguments:** Prevents using `-o` with `-r` (recursive mode)

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library modules)

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
</div>
#end def

#def iframeCard($name)
#set iframe_url = $getVar('Extras.Embedded.' + name + '.url', "")
#set iframe_title = $getVar('Extras.Embedded.' + name + '.title', "")
#set iframe_aspect = $getVar('Extras.Embedded.' + name + '.aspect_ratio', "4/3")
#if iframe_url != ""
<div class="col-12 col-md-6 col-xl-4 mb-4">
<div class="card overflow-hidden">
<div class="card-body text-center d-flex flex-column px-0 ${'pb-0' if iframe_title != '' else 'py-0'} overflow-hidden">
#if iframe_title != ""
<h5 class="h5-responsive $Extras.color-text">
    $iframe_title
</h5>
#end if
<iframe src="$iframe_url" frameborder="0" class="flex-grow-1 w-100" style="aspect-ratio: ${iframe_aspect};"></iframe>
</div>
</div>
</div>
#else
$notFoundCard($name)
#end if
#end def
```

### After

```html
#def notFoundCard($name)
    <div class="col-12 col-md-6 col-xl-4 mb-4">
        <div class="card">
            <div class="card-body text-center">
                Section definition not found for "$name"
            </div>
        </div>
    </div>
#end def

#def iframeCard($name)
    #set iframe_url = $getVar('Extras.Embedded.' + name + '.url', "")
    #set iframe_title = $getVar('Extras.Embedded.' + name + '.title', "")
    #set iframe_aspect = $getVar('Extras.Embedded.' + name + '.aspect_ratio', "4/3")
    #if iframe_url != ""
        <div class="col-12 col-md-6 col-xl-4 mb-4">
            <div class="card overflow-hidden">
                <div class="card-body text-center d-flex flex-column px-0 ${'pb-0' if iframe_title != '' else 'py-0'} overflow-hidden">
                    #if iframe_title != ""
                        <h5 class="h5-responsive $Extras.color-text">
                            $iframe_title
                        </h5>
                    #end if
                    <iframe src="$iframe_url" frameborder="0" class="flex-grow-1 w-100" style="aspect-ratio: ${iframe_aspect};"></iframe>
                </div>
            </div>
        </div>
    #else
        $notFoundCard($name)
    #end if
#end def
```
