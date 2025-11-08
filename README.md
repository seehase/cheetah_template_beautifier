# Cheetah Template Beautifier

This script reformats Cheetah templates to improve readability by adjusting indentation for HTML, Cheetah directives, and embedded Javascript code. It helps maintain a consistent code style across your templates, making them easier to read and maintain.

## Features

- **Smart Indentation:** Automatically adjusts indentation for HTML tags, Cheetah directives (`#if`, `#for`, etc.), and Javascript blocks.
- **Void Element Handling:** Correctly handles HTML void elements (e.g., `<br>`, `<img>`) that don't have closing tags.
- **File Processing:** Can process a single file or recursively find and reformat all `.tmpl` files in a directory.
- **In-place or Output File:** You can either reformat a file in-place or write the output to a new file.

## Usage

### Basic Usage

To reformat a single template file in-place:

```bash
python cheetah_template_beautifier.py /path/to/your/template.tmpl
```

### Output to a Different File

To reformat a template and save the output to a new file:

```bash
python cheetah_template_beautifier.py /path/to/your/template.tmpl -o /path/to/output.tmpl
```

### Recursive Reformatting

To recursively find and reformat all `.tmpl` files in a directory:

```bash
python cheetah_template_beautifier.py /path/to/your/templates/ -r
```

## Before and After

Here is an example of a Cheetah template before and after reformatting:

### Before

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
