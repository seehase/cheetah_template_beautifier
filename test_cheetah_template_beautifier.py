#!/usr/bin/env python3
import unittest
import tempfile
import os
import shutil
import sys
from unittest.mock import patch, mock_open, MagicMock
from io import StringIO

# Add the current directory to the Python path so we can import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cheetah_template_beautifier import reformat_cheetah_template, process_file, main


class TestCheetahTemplateBeautifier(unittest.TestCase):

    def test_html_indentation(self):
        """Test basic HTML tag indentation."""
        source = "<div>\n<p>Hello</p>\n</div>"
        expected = "<div>\n    <p>Hello</p>\n</div>"
        result = reformat_cheetah_template(source)
        self.assertEqual(result, expected)

    def test_nested_html_indentation(self):
        """Test nested HTML tag indentation."""
        source = "<div>\n<div>\n<p>Nested</p>\n</div>\n</div>"
        expected = "<div>\n    <div>\n        <p>Nested</p>\n    </div>\n</div>"
        result = reformat_cheetah_template(source)
        self.assertEqual(result, expected)

    def test_void_elements(self):
        """Test that void elements don't affect indentation."""
        source = "<div>\n<img src='test.jpg'>\n<p>Text</p>\n</div>"
        expected = "<div>\n    <img src='test.jpg'>\n    <p>Text</p>\n</div>"
        result = reformat_cheetah_template(source)
        self.assertEqual(result, expected)

    def test_self_closing_tags(self):
        """Test self-closing HTML tags."""
        source = "<div>\n<input type='text' />\n<p>Text</p>\n</div>"
        expected = "<div>\n    <input type='text' />\n    <p>Text</p>\n</div>"
        result = reformat_cheetah_template(source)
        self.assertEqual(result, expected)

    def test_cheetah_if_directive(self):
        """Test Cheetah #if directive indentation."""
        source = "#if $condition\n<p>Content</p>\n#end if"
        expected = "#if $condition\n    <p>Content</p>\n#end if"
        result = reformat_cheetah_template(source)
        self.assertEqual(result, expected)

    def test_cheetah_for_directive(self):
        """Test Cheetah #for directive indentation."""
        source = "#for $item in $items\n<li>$item</li>\n#end for"
        expected = "#for $item in $items\n    <li>$item</li>\n#end for"
        result = reformat_cheetah_template(source)
        self.assertEqual(result, expected)

    def test_cheetah_def_directive(self):
        """Test Cheetah #def directive indentation."""
        source = "#def myFunction()\n<p>Function content</p>\n#end def"
        expected = "#def myFunction()\n    <p>Function content</p>\n#end def"
        result = reformat_cheetah_template(source)
        self.assertEqual(result, expected)

    def test_cheetah_else_directive(self):
        """Test Cheetah #else directive indentation."""
        source = "#if $condition\n<p>True</p>\n#else\n<p>False</p>\n#end if"
        expected = "#if $condition\n    <p>True</p>\n#else\n    <p>False</p>\n#end if"
        result = reformat_cheetah_template(source)
        self.assertEqual(result, expected)

    def test_cheetah_elif_directive(self):
        """Test Cheetah #elif directive indentation."""
        source = "#if $a\n<p>A</p>\n#elif $b\n<p>B</p>\n#end if"
        expected = "#if $a\n    <p>A</p>\n#elif $b\n    <p>B</p>\n#end if"
        result = reformat_cheetah_template(source)
        self.assertEqual(result, expected)

    def test_cheetah_else_if_directive(self):
        """Test Cheetah #else if directive indentation."""
        source = "#if $a\n<p>A</p>\n#else if $b\n<p>B</p>\n#end if"
        expected = "#if $a\n    <p>A</p>\n#else if $b\n    <p>B</p>\n#end if"
        result = reformat_cheetah_template(source)
        self.assertEqual(result, expected)

    def test_javascript_indentation(self):
        """Test JavaScript code block indentation."""
        source = "function test() {\nvar x = 1;\nif (x) {\nconsole.log('test');\n}\n}"
        expected = "function test() {\n    var x = 1;\n    if (x) {\n        console.log('test');\n    }\n}"
        result = reformat_cheetah_template(source)
        self.assertEqual(result, expected)

    def test_javascript_with_arrays(self):
        """Test JavaScript arrays indentation."""
        source = "var arr = [\n'item1',\n'item2'\n];"
        expected = "var arr = [\n    'item1',\n    'item2'\n];"
        result = reformat_cheetah_template(source)
        self.assertEqual(result, expected)

    def test_mixed_cheetah_html(self):
        """Test mixed Cheetah directives and HTML."""
        source = "#if $user\n<div>\n<p>Hello $user.name</p>\n</div>\n#end if"
        expected = "#if $user\n    <div>\n        <p>Hello $user.name</p>\n    </div>\n#end if"
        result = reformat_cheetah_template(source)
        self.assertEqual(result, expected)

    def test_multiline_tag(self):
        """Test multiline HTML tag handling - current behavior preserves structure."""
        source = "<div class='test'\nid='myid'>\n<p>Content</p>\n</div>"
        # Note: Current implementation doesn't indent content inside multiline tags
        # This might be improved in future versions
        expected = "<div class='test'\nid='myid'>\n<p>Content</p>\n</div>"
        result = reformat_cheetah_template(source)
        self.assertEqual(result, expected)

    def test_cheetah_variables_in_js(self):
        """Test that Cheetah variables in JavaScript don't affect indentation."""
        source = "var name = '${user.name}';\nif (name) {\nconsole.log(name);\n}"
        expected = "var name = '${user.name}';\nif (name) {\n    console.log(name);\n}"
        result = reformat_cheetah_template(source)
        self.assertEqual(result, expected)

    def test_empty_lines_cleanup(self):
        """Test that multiple consecutive empty lines are reduced to one."""
        source = "<div>\n\n\n<p>Test</p>\n\n\n</div>"
        expected = "<div>\n\n    <p>Test</p>\n\n</div>"
        result = reformat_cheetah_template(source)
        self.assertEqual(result, expected)

    def test_complex_nested_structure(self):
        """Test complex nested structure with multiple types."""
        source = "#if $condition\n<div>\n#for $item in $items\n<ul>\n<li>$item</li>\n</ul>\n#end for\n</div>\n#end if"
        expected = "#if $condition\n    <div>\n        #for $item in $items\n            <ul>\n                <li>$item</li>\n            </ul>\n        #end for\n    </div>\n#end if"
        result = reformat_cheetah_template(source)
        self.assertEqual(result, expected)

    def test_no_indentation_change_for_plain_text(self):
        """Test that plain text lines don't affect indentation."""
        source = "Some plain text\nMore plain text"
        expected = "Some plain text\nMore plain text"
        result = reformat_cheetah_template(source)
        self.assertEqual(result, expected)

    def test_preserve_existing_empty_lines(self):
        """Test that single empty lines are preserved."""
        source = "<div>\n\n<p>Test</p>\n</div>"
        expected = "<div>\n\n    <p>Test</p>\n</div>"
        result = reformat_cheetah_template(source)
        self.assertEqual(result, expected)

    @patch('builtins.open', new_callable=mock_open, read_data='<div>\n<p>Test</p>\n</div>')
    @patch('builtins.print')
    def test_process_file_success(self, mock_print, mock_file):
        """Test successful file processing."""
        process_file('test.tmpl')
        mock_print.assert_called_with('Successfully reformatted test.tmpl and saved to test.tmpl')

    @patch('builtins.open', new_callable=mock_open, read_data='<div>\n<p>Test</p>\n</div>')
    @patch('builtins.print')
    def test_process_file_with_outfile(self, mock_print, mock_file):
        """Test file processing with separate output file."""
        process_file('test.tmpl', 'output.tmpl')
        mock_print.assert_called_with('Successfully reformatted test.tmpl and saved to output.tmpl')

    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('builtins.print')
    def test_process_file_not_found(self, mock_print, mock_file):
        """Test file not found error handling."""
        process_file('nonexistent.tmpl')
        mock_print.assert_called_with('Error: Source file not found at nonexistent.tmpl')

    @patch('builtins.open', new_callable=mock_open)
    @patch('builtins.print')
    def test_process_file_write_error(self, mock_print, mock_file):
        """Test write error handling."""
        mock_file.side_effect = [mock_open(read_data='<div></div>').return_value, IOError("Permission denied")]
        process_file('test.tmpl')
        mock_print.assert_called_with('Error writing to output file: Permission denied')

    def test_main_recursive_both_extensions(self):
        """Test that recursive mode processes both .tmpl and .inc files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            tmpl_file = os.path.join(temp_dir, 'test.tmpl')
            inc_file = os.path.join(temp_dir, 'test.inc')
            other_file = os.path.join(temp_dir, 'test.txt')

            test_content = '<div>\n<p>Test</p>\n</div>'

            with open(tmpl_file, 'w') as f:
                f.write(test_content)
            with open(inc_file, 'w') as f:
                f.write(test_content)
            with open(other_file, 'w') as f:
                f.write(test_content)

            with patch('sys.argv', ['script', '-r', temp_dir]):
                with patch('builtins.print') as mock_print:
                    main()

            # Check that both .tmpl and .inc files were processed
            with open(tmpl_file, 'r') as f:
                tmpl_result = f.read()
            with open(inc_file, 'r') as f:
                inc_result = f.read()
            with open(other_file, 'r') as f:
                other_result = f.read()

            expected = '<div>\n    <p>Test</p>\n</div>'
            self.assertEqual(tmpl_result, expected)
            self.assertEqual(inc_result, expected)
            self.assertEqual(other_result, test_content)  # Should be unchanged

    def test_main_recursive_subdirectories(self):
        """Test that recursive mode processes files in subdirectories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create subdirectory structure
            sub_dir = os.path.join(temp_dir, 'subdir')
            os.makedirs(sub_dir)

            tmpl_file = os.path.join(sub_dir, 'nested.tmpl')
            test_content = '<div>\n<p>Nested</p>\n</div>'

            with open(tmpl_file, 'w') as f:
                f.write(test_content)

            with patch('sys.argv', ['script', '-r', temp_dir]):
                with patch('builtins.print') as mock_print:
                    main()

            # Check that nested file was processed
            with open(tmpl_file, 'r') as f:
                result = f.read()

            expected = '<div>\n    <p>Nested</p>\n</div>'
            self.assertEqual(result, expected)

    @patch('sys.argv', ['script', '--help'])
    def test_main_no_source(self):
        """Test main function with no source argument."""
        with patch('argparse.ArgumentParser.print_help') as mock_help:
            with self.assertRaises(SystemExit):
                main()

    @patch('sys.argv', ['script', '-r', 'nonexistent'])
    @patch('builtins.print')
    def test_main_recursive_invalid_dir(self, mock_print):
        """Test recursive mode with invalid directory."""
        main()
        mock_print.assert_any_call('Error: --recursive requires a valid directory path.')

    @patch('sys.argv', ['script', '-r', '-o', 'output.tmpl', '/tmp'])
    @patch('builtins.print')
    def test_main_recursive_with_outfile_error(self, mock_print):
        """Test recursive mode with outfile argument (should error)."""
        main()
        mock_print.assert_any_call('Error: -o/--outfile cannot be used with --recursive.')

    def test_main_single_file(self):
        """Test main function with single file processing."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tmpl', delete=False) as temp_file:
            temp_file.write('<div>\n<p>Test</p>\n</div>')
            temp_file_path = temp_file.name

        try:
            with patch('sys.argv', ['script', temp_file_path]):
                with patch('builtins.print') as mock_print:
                    main()

            # Check that file was processed
            with open(temp_file_path, 'r') as f:
                result = f.read()

            expected = '<div>\n    <p>Test</p>\n</div>'
            self.assertEqual(result, expected)
        finally:
            os.unlink(temp_file_path)

    @patch('sys.argv', ['script', 'nonexistent.tmpl'])
    @patch('builtins.print')
    def test_main_single_file_not_found(self, mock_print):
        """Test main function with non-existent file."""
        main()
        mock_print.assert_any_call('Error: Source file not found at nonexistent.tmpl')

    @patch('sys.argv', ['script', '--version'])
    def test_main_version(self):
        """Test version argument."""
        with self.assertRaises(SystemExit):
            main()

    def test_complex_javascript_structure(self):
        """Test complex JavaScript structure with nested objects and arrays."""
        source = "var config = {\napi: {\nurl: 'http://example.com',\nheaders: [\n'Content-Type: application/json',\n'Authorization: Bearer token'\n]\n}\n};"
        expected = "var config = {\n    api: {\n        url: 'http://example.com',\n        headers: [\n            'Content-Type: application/json',\n            'Authorization: Bearer token'\n        ]\n    }\n};"
        result = reformat_cheetah_template(source)
        self.assertEqual(result, expected)

    def test_mixed_js_and_html(self):
        """Test mixed JavaScript and HTML content."""
        source = "<script>\nfunction init() {\nvar elem = document.getElementById('test');\nif (elem) {\nelem.innerHTML = 'Hello';\n}\n}\n</script>"
        expected = "<script>\n    function init() {\n        var elem = document.getElementById('test');\n        if (elem) {\n            elem.innerHTML = 'Hello';\n        }\n    }\n</script>"
        result = reformat_cheetah_template(source)
        self.assertEqual(result, expected)

    def test_cheetah_nested_structures(self):
        """Test deeply nested Cheetah structures."""
        source = "#if $users\n#for $user in $users\n#if $user.active\n<div>\n<p>$user.name</p>\n#if $user.admin\n<span>Admin</span>\n#end if\n</div>\n#end if\n#end for\n#end if"
        expected = "#if $users\n    #for $user in $users\n        #if $user.active\n            <div>\n                <p>$user.name</p>\n                #if $user.admin\n                    <span>Admin</span>\n                #end if\n            </div>\n        #end if\n    #end for\n#end if"
        result = reformat_cheetah_template(source)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
