# :pushpin: :lock: Certificate :pushpin: :lock:
A repository for known pinned certificates hostnames out on the internet.

# tl;dr
Download the file relevant to your needs:
* The `compiled-with-headers.txt` file contains the headers and hostnames to help navigate the list.
* The `sorted-without-headers.txt` file contains only the hostnames.

# Directory Structure
```
data/
  -> category/
     -> application-name/
        -> hostnames
        -> header
```
* The `hostnames` file contains a list of known hostnames that use certificate pinning
* The `header` file contains a header that is appended into the `compiled.txt` file when compilation of all contents of the data parsed.


# Contributions
If you would like to contribute to this list, please feel to create a pull request and submit the following information to support the request:
* Vendor
* Application Name
* Application Category - ideally use one of the existing categories defined, but opent to creating a new one.
* Public URL (if applicable) that mentions pinned certificate hostnames or wildcard domains.
* (Optional/Preferred) Wireshark capture showing the TLS handshake failing and the Fatal error. Need to see the hostname being established in the handshake to make a correlation.
