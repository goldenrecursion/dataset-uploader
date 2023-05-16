# Dataset Uploader

## About this fork
This was an attempt I'd made a while ago at a webapp that progresses towards this proposed dataset uploader's goals (See below or `SPECS.md`). 

Currently, it's a base Django app that allows users to log in with their Metamask ethereum addresses (has to be the same one they've used to create an account on the Golden dApp) and sign an authentication message via Godel (Golden's Python SDK for its API) to get a JWT to authenticate/initialize the Golden API. This (JWT) is then stored locally until it expires (then the user is prompted to sign a message again to get a new JWT) and can be used for further authentication with the API for data upload, disambiguation, and other functions where the Golden API has to be used. 

With recent developments (a Nous Labs spin off from Golden), no-code user data upload may not be necessary right now, but maybe this could be repurposed for other needs. 

## Set up/Installation

Some settings in `src/golden_dataset_uploader/settings.py` can be edited as required. 

Build an image with `docker build -t <image-name> .` 

Spin up a container and visit localhost:8000 to view and test. 

## Overview
Golden is a decentralized graph of canonical knowledge that is open, free, permissionless, and incentivizes contributions with the aim to map all of human knowledge. 

This Dataset Uploader will provide users with a no-code solution to import datasets to the graph.

## Contributing
Contributions are welcome! Please refer to `CONTRIBUTING.md` and `SPECS.md` for more information, the latter of which includes a vision of product and technical requirements as well as example use cases.   

## Contact
For matters related to this repository, please contact the maintainer Katrina Pettitt at kat@golden.co or [@katkaypettitt](https://twitter.com/katkaypettitt) for any questions or comments. 

For all other support, please reach out to support@golden.co.

Follow [@golden](https://twitter.com/Golden) to keep up with additional news!

## License
This project is licensed under the terms of the Apache 2.0 license. 
