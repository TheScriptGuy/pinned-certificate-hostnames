# 2024-02-09
## Enhancements :rocket:
* Added a print statement to `compile.py` to display the number of hostnames found in the hostnames files.
* Added a sha256 hash calculation of the `compiled-with-comments.txt` and `compiled-without-comments.txt`. Hashes are added to `file-validation.hash`.
* Added several other pinned certificate websites.


# 2024-02-07
## Enhancements :rocket:
* Added `compile.py` to recursively walk through a supplied directory and build 2 files:
  * `compiled-with-comments.txt` which is a concatenation of all the header and hostnames files
  * `compiled-without-comments.txt` which only lists the hostnames that need to be excluded.
