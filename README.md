# A Personal Blog

## Blog site setup for publishing to Github



## Setup

Follow quickstart at: https://gohugo.io/getting-started/quick-start/

### How to clone a copy

	> git clone <path>

### Need to clone theme

	> git submodule add https://github.com/sudorook/capsule themes/capsule


## Operation

### Adding a post

Posts are in the content/ directory.  There can be subfolders there for different types of content although the folders are not maintained in the published site, they are purely for organization of the posts.

A post can be a simple markdown file or a folder which contains a markdown file along with the images for the post.  Using this structure, each post is self contained.  If the post is in a folder it should be in a file named **index.md**. If it is a stand-alone file it can have any unique name.

The header of the markdown file contains a specific header that is used to determine the categories and tags used on the site as well as the publishing date of the post.  The format of this header is:

```
slug: "slug-name"
title: "title for the post"
date: yyyy-mm-dd
draft: false
tags:
- tag1
- tag2
categories
- category1
```

Current categories are "Travel".

### Build static site

	> hugo
	
### Preview the site

   > hugo server
   
### Publishing the site
