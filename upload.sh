#!/bin/bash
zip config -yr .
mv config.zip $blog_dir/home/media/
cd $blog_dir/home
epost auto
