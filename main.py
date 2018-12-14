#!/usr/bin/env python3
import collections, os, shutil, subprocess

# TODO
# There are many bugs related to the ordering of replace() calls.
# They should not have impact in most cases

def strip_split(s, delim):
    return [s.strip() for s in s.split(delim)]

def parse_post(post_text):
    header_text, body = post_text.split("\n---\n", 1)
    headers = {}
    for line in header_text.split("\n"):
        if line.count(":") == 1:
            key, val = strip_split(line, ":")
            assert(key not in headers.keys())
            headers[key] = val
    return (headers, body)

def make_html(template, title, body):
    template = template.replace("{{title}}", title)
    template = template.replace("{{content}}", body)
    return template

def md_to_html(md):
    pd = os.path.join(os.path.dirname(os.path.realpath(__file__)), "bin/pandoc")
    output = subprocess.run(
        [pd, "--from=markdown", "--to=html"],
        stdout=subprocess.PIPE,
        input=md,
        encoding="utf-8")
    assert(output.returncode == 0)
    return output.stdout

def main():
    base_path = os.path.dirname(os.path.realpath(__file__))
    post_template = open(os.path.join(base_path, "post.html")).read()
    passthrough_files = ["index.html", "style.css", "CNAME"]

    posts = []
    for f in os.listdir(os.path.join(base_path, "posts/")):
        file_text = open(os.path.join(base_path, "posts/", f)).read()
        headers, body = parse_post(file_text)
        body_html = md_to_html(body)
        html = make_html(post_template, headers["title"], body_html)
        posts.append(
            {
                "url": headers["url"],
                "html": html,
            }
        )

    outdir = os.path.join(base_path, "out/")
    shutil.rmtree(outdir, ignore_errors=True)
    os.makedirs(outdir, exist_ok=True)

    for f in passthrough_files:
        shutil.copy(os.path.join(base_path, f), outdir)

    for post in posts:
        os.makedirs(os.path.join(outdir, post["url"]))
        with open(os.path.join(outdir, post["url"], "index.html"), "w") as post_file:
            post_file.write(post["html"])

if __name__ == "__main__":
    main()
