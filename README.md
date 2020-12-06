# parade
parade is a encoder/decoder of data using image file.

### Getting Started
**install**
```bash
pip install git+https://github.com/TakutoYoshikai/parade.git
```
**encode**
```bash
parade encode -i <image FILE> -d <secret data FILE> -o <output key FILE>
```

**decode**
```bash
parade decode -i <image FILE> -k <key FILE> -s <SIZE of secret data> -o <output data FILE>
```

### License
MIT License
