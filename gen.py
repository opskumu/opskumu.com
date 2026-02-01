#!/usr/bin/env python3
"""Static site generator for converting Markdown to HTML."""

import os
import shutil
import subprocess
from pathlib import Path
from string import Template
from typing import List
import mistune


class SiteGenerator:
    """Static site generator for Markdown files."""
    
    def __init__(self, root_dir: str = ".", dist_dir: str = "dist"):
        self.root_dir = Path(root_dir).resolve()
        self.dist_dir = self.root_dir / dist_dir
        self.assets_dir = self.dist_dir / "assets"
        self.template_file = self.root_dir / "template.html"

    def create_output_dir(self) -> None:
        """Create the output directory, removing existing one if it exists."""
        try:
            if self.dist_dir.exists():
                print(f"[{self.dist_dir}] exists, deleting it")
                shutil.rmtree(self.dist_dir)
            
            self.dist_dir.mkdir(parents=True)
            self.assets_dir.mkdir(exist_ok=True)
            print(f"Created output directory: {self.dist_dir}")
        except OSError as e:
            raise RuntimeError(f"Failed to create output directory: {e}")

    def copy_static_files(self) -> None:
        """Copy static files (index.html, images, favicon) to dist directory."""
        try:
            static_files = [
                ("index.html", self.dist_dir / "index.html"),
                ("assets/avatar.png", self.assets_dir / "avatar.png"),
                ("assets/favicon.ico", self.assets_dir / "favicon.ico"),
            ]
            
            for src, dst in static_files:
                src_path = self.root_dir / src
                if src_path.exists():
                    shutil.copy2(src_path, dst)
                    print(f"Copied {src} to {dst}")
                else:
                    print(f"Warning: {src} not found, skipping")
        except OSError as e:
            raise RuntimeError(f"Failed to copy static files: {e}")

    def compile_styles(self) -> None:
        """Compile LESS to CSS using lessc compiler."""
        lessc = shutil.which("lessc")
        if not lessc:
            raise RuntimeError("lessc compiler not found in PATH")
        
        src_less = self.root_dir / "assets" / "style.less"
        dst_css = self.assets_dir / "style.css"
        
        if not src_less.exists():
            print(f"Warning: {src_less} not found, skipping style compilation")
            return
        
        try:
            cmd = [lessc, str(src_less), str(dst_css)]
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"Compiled styles: {src_less} -> {dst_css}")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to compile styles: {e.stderr}")
        except FileNotFoundError:
            raise RuntimeError("lessc command not found")

    def load_template(self) -> Template:
        """Load HTML template from file."""
        try:
            with open(self.template_file, "r", encoding="utf-8") as f:
                template_content = f.read()
            return Template(template_content)
        except FileNotFoundError:
            raise RuntimeError(f"Template file not found: {self.template_file}")

    def convert_markdown_files(self, md_files: List[str]) -> None:
        """Convert Markdown files to HTML using the template."""
        template = self.load_template()
        
        for md_file in md_files:
            md_path = self.root_dir / md_file
            if not md_path.exists():
                print(f"Warning: {md_file} not found, skipping")
                continue
            
            try:
                with open(md_path, "r", encoding="utf-8") as f:
                    md_content = f.read()
                
                html_content = mistune.markdown(md_content)
                final_html = template.substitute(content=html_content)
                
                output_name = md_path.stem + ".html"
                output_path = self.dist_dir / output_name
                
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(final_html)
                
                print(f"Converted {md_file} -> {output_name}")
            except (OSError, UnicodeDecodeError) as e:
                print(f"Error processing {md_file}: {e}")

    def find_markdown_files(self) -> List[str]:
        """Find all Markdown files in the root directory."""
        md_files = []
        for file_path in self.root_dir.glob("*.md"):
            if file_path.name != "README.md":
                md_files.append(file_path.name)
        return md_files

    def generate(self) -> None:
        """Generate the complete static site."""
        try:
            self.create_output_dir()
            self.copy_static_files()
            self.compile_styles()
            
            md_files = self.find_markdown_files()
            if md_files:
                self.convert_markdown_files(md_files)
            else:
                print("No Markdown files found to convert")
            
            print("Site generation completed successfully!")
        except Exception as e:
            print(f"Error during site generation: {e}")
            raise


if __name__ == "__main__":
    generator = SiteGenerator()
    generator.generate()
