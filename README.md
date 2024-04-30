# python

## Getting Started

### 1. Clone & Prepare .env

```sh
$ git clone git@github.com:nglcobdai/python-template.git
$ cd python-template
```

### 2. Create .env

- copy .env.example to .env

```sh
$ cp .env{.example,}
```

### 3. Docker Build & Run

```sh
docker-compose build --no-cache
docker-compose run --rm project /bin/bash
```
