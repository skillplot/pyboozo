# PyBoozo

Python based command line utility for bare bone software development directory structure setup and configuration generator.

```bash
                          _,..,,,_
                     '``````^~"-,_`"-,_
       .-~c~-.                    `~:. ^-.
   `~~~-.c    ;                      `:.  `-,     _.-~~^^~:.
         `.   ;      _,--~~~~-._       `:.   ~. .~          `.
          .` ;'   .:`           `:       `:.   `    _.:-,.    `.
        .' .:   :'    _.-~^~-.    `.       `..'   .:      `.    '
       :  .' _:'   .-'        `.    :.     .:   .'`.        :    ;
       :  `-'   .:'             `.    `^~~^`   .:.  `.      ;    ;
        `-.__,-~                  ~-.        ,' ':    '.__.`    :'
                                     ~--..--'     ':.         .:'
                                                     ':..___.:'
```

PyBoozo is an opinionated software development environment setup and configuration generator.
It provides the bare bone directory structure for setting up software development environment. It generate respective configurations, environment variables to be used across seamlessly.

These conventions and configurations can easily be customized or extended. The created directory structures gives you the barebone development environment with required configuration files.

These convention of directories and choices let you work with docker containers and host system in parallel, such that all the data and code remains outside the containers, but separate configuration gets generated inside the containers still pointing out to the same relative and absolute paths.

## Highlights

* Core separate components (directories):
  1. Code
  2. Data
  3. Configurations
  4. Mobile
  5. Virtualenv
* **Auto configuration generation:**
  * `<name>.yml` -> load this file from any application code; this has one-to-one-mapping with environment variables
  * `<name>.export.sh` -> all the path and required environment variables for command line setup
  * `<name>.alias.sh` -> useful shortcuts for directory navigation
  * `<name>.env.sh` -> include the `export` and `alias` scripts. This is the single file to be included inside the `~/.bashrc` file as:
    ```bash
    source /<name>-hub/<name>/config/<name>.env.sh
    ```
  * **NOTE:**
    * `<name>` is the name given by you at the time of project setup; default name is: `boozo`
* This directory is meant to work seamlessly with stateless docker containers
  * Sharing the host's directories having code, data and virtualenv with the docker container (using Volume mapping)
    * This allows the docker container to be completely stateless yet fully functional
  * The configuration files (.yml and .sh) are separate between host and docker
    * This ensures docker container are only loosely coupled to host and allows to change the application behavior independent to the host system
  * One example is having separate CUDA version nvidia gpu docker containers for ML/AI and computer vision development, but everything resides on host system - this saves unnecessary duplication installation/un-installation of python dependencies / virtualenvs
* Interactive failsafe system setup
* Consistent conventions allows sharing with others in the team or otherwise less painful

**NOTE:**
* Only Linux is supported (Tested on Ubuntu 18.04 LTS)
* `.sh` files are tested for `bash` shell.


## Setup

**NOTE:**
* Creating a application root directory manually in the system root `/` and using that for setup is recommended as it provides username independent configurations and allows to seamlessly across physical systems and docker containers.

* To create at `/` level; first create top level directory and give the user level permission, before running the script
```bash
sudo mkdir -p /boozo-hub && sudo chown -R $(id -u):$(id -g) /boozo-hub
cd /
boozo
```
This will create the required directory structure and generate the configuration files.

**NOTE:**
* name supports only `a-z`, `/` and `-`; maximum 7 chars long names
* prefix is only `a-z` and maximum 3 chars long; implicitly `_` will be appended to the prefix automatically
* `--gitkeep` creates empty .gitkeep file in each directory
* `--timestamp` creates timestamped based data directory symlinked to common name, allows to easily link to different mount partitions by changing the symlinks
* `--name` and `--prefix` options provides for the unique namespace and configurations;
* more the one stack can be setup within the same application root directory provided it has all apps have unique name space i.e. `unique name` and `unique prefix`. This is the recommended
  * A single unique name space generates unique directories, configuration filenames, environment variables, aliases
* Avoid using default name and prefix for custom application setup
* A pre-configured `.gitignore` file will be created for the main app folder: `/boozo-hub/boozo`
* Once setup is done, `git init` is required to initialize the main application directory i.e. `/boozo-hub/boozo`


### Setup using pip package

* Install pip package:
  ```bash
  pip install pyboozo
  ```
* Create new project setup
  ```bash
  ## check the help menu for options
  boozo --help
  ## run interactively
  boozo
  ## different silent execution
  boozo --root=/boozo-hub --name=boozo --prefix=bzo
  boozo --root=/boozo-hub --name=boozo --prefix=bzo --gitkeep
  boozo --root=/boozo-hub --name=boozo --prefix=bzo --gitkeep --timestamp
  ```

### Setup using source code

* Clone the git repo
* Execute from the cloned source code
  ```bash
  python -m boozo
  ```

## How the directory structure looks like?

**NOTE:**
* Application root directory name (`/boozo-hub`)can be anything and different than the app name (`boozo`)
* Providing the appname provides unique 4 directories bound to the app name: `boozo`, `boozo-dat`, `boozo-mobile` and `boozo-config`
* More then one appname can be setup given that they have different app name. but same application root directory. This can be given at the time of running the project setup installer.
* Observe the use of soft links that separates the code with the data, logs and mobile sdks.
* while creating stateless docker container, map only the directories: `boozo`, `boozo-dat`, `boozo-mobile`, and `virtualmachines`
  * Do NOT map `boozo-config` directory to the docker container, instead run the `pyboozo` again inside the container to generate new configuration that lives inside the container only and separate from host
  * For all application usage use only the environment variables with `*HOME` suffix instead of `*ROOT` suffix. The difference is all the `*HOME` suffix variables are the soft link inside the main application, in the example `boozo/config`.
* A default `.gitignore` is provided as the starting point; if it's already exists it will NOT be overridden.


### Directory Stack - Minimal view

The directory and files created (minimal view)

```bash
boozo-hub/
├── boozo
│   ├── apps
│   ├── common
│   ├── config -> /boozo-hub/boozo-config
│   ├── data -> /boozo-hub/boozo-dat
│   ├── dist
│   ├── docs
│   ├── logs -> /boozo-hub/boozo/data/logs
│   ├── mobile -> /boozo-hub/boozo-mobile
│   ├── plugins
│   ├── practice
│   ├── scripts
│   ├── tests
│   ├── tmp -> /boozo-hub/boozo/data/tmp
│   ├── virtualenvs -> /boozo-hub/virtualmachines/virtualenvs
│   └── www
├── boozo-config
│   ├── boozo.alias.sh
│   ├── boozo.env.sh
│   ├── boozo.export.sh
│   └── boozo.yml
├── boozo-dat
│   ├── aid
│   │   └── tfrecords
│   ├── ant
│   ├── auth
│   ├── cfg
│   ├── cloud
│   ├── databases
│   │   └── mongodb
│   │       ├── configdb
│   │       ├── db
│   │       ├── key
│   │       └── logs
│   ├── docker
│   ├── downloads
│   ├── external
│   ├── kbank
│   ├── logs
│   │   └── www
│   ├── mnt
│   ├── mobile
│   ├── npm-packages
│   ├── public
│   ├── public_html
│   ├── release
│   │   ├── keras
│   │   └── torch
│   ├── reports
│   ├── samples
│   ├── _site
│   ├── team
│   │   └── images
│   ├── tmp
│   ├── tools
│   ├── uploads
│   └── workspaces
├── boozo-mobile
│   └── android
│       ├── apps
│       ├── dist
│       ├── external
│       ├── plugins
│       └── sdk
└── virtualmachines
    └── virtualenvs

62 directories, 4 files
```

### Directory Stack - Complete Expanded view

The directory and files created (Complete Expanded view, shown for non-timestamped data directory setup)

```bash
boozo-hub/
├── boozo
│   ├── apps
│   │   └── .gitkeep
│   ├── common
│   │   └── .gitkeep
│   ├── config -> /boozo-hub/boozo-config
│   │   ├── boozo.alias.sh
│   │   ├── boozo.env.sh
│   │   ├── boozo.export.sh
│   │   ├── boozo.yml
│   │   └── .gitkeep
│   ├── data -> /boozo-hub/boozo-dat
│   │   ├── aid
│   │   │   ├── .gitkeep
│   │   │   └── tfrecords
│   │   │       └── .gitkeep
│   │   ├── ant
│   │   │   └── .gitkeep
│   │   ├── auth
│   │   │   └── .gitkeep
│   │   ├── cfg
│   │   │   └── .gitkeep
│   │   ├── cloud
│   │   │   └── .gitkeep
│   │   ├── databases
│   │   │   ├── .gitkeep
│   │   │   └── mongodb
│   │   │       ├── configdb
│   │   │       │   └── .gitkeep
│   │   │       ├── db
│   │   │       │   └── .gitkeep
│   │   │       ├── .gitkeep
│   │   │       ├── key
│   │   │       │   └── .gitkeep
│   │   │       └── logs
│   │   │           └── .gitkeep
│   │   ├── docker
│   │   │   └── .gitkeep
│   │   ├── downloads
│   │   │   └── .gitkeep
│   │   ├── external
│   │   │   └── .gitkeep
│   │   ├── kbank
│   │   │   └── .gitkeep
│   │   ├── logs
│   │   │   ├── .gitkeep
│   │   │   └── www
│   │   │       └── .gitkeep
│   │   ├── mnt
│   │   │   └── .gitkeep
│   │   ├── mobile
│   │   │   └── .gitkeep
│   │   ├── npm-packages
│   │   │   └── .gitkeep
│   │   ├── public
│   │   │   └── .gitkeep
│   │   ├── public_html
│   │   │   └── .gitkeep
│   │   ├── release
│   │   │   ├── .gitkeep
│   │   │   ├── keras
│   │   │   │   └── .gitkeep
│   │   │   └── torch
│   │   │       └── .gitkeep
│   │   ├── reports
│   │   │   └── .gitkeep
│   │   ├── samples
│   │   │   └── .gitkeep
│   │   ├── _site
│   │   │   └── .gitkeep
│   │   ├── team
│   │   │   ├── .gitkeep
│   │   │   └── images
│   │   │       └── .gitkeep
│   │   ├── tmp
│   │   │   └── .gitkeep
│   │   ├── tools
│   │   │   └── .gitkeep
│   │   ├── uploads
│   │   │   └── .gitkeep
│   │   └── workspaces
│   │       └── .gitkeep
│   ├── dist
│   │   └── .gitkeep
│   ├── docs
│   │   └── .gitkeep
│   ├── .gitignore
│   ├── logs -> /boozo-hub/boozo/data/logs
│   ├── mobile -> /boozo-hub/boozo-mobile
│   │   └── android
│   │       ├── apps
│   │       │   └── .gitkeep
│   │       ├── dist
│   │       │   └── .gitkeep
│   │       ├── external
│   │       │   └── .gitkeep
│   │       ├── .gitkeep
│   │       ├── plugins
│   │       │   └── .gitkeep
│   │       └── sdk
│   │           └── .gitkeep
│   ├── plugins
│   │   └── .gitkeep
│   ├── practice
│   │   └── .gitkeep
│   ├── scripts
│   │   └── .gitkeep
│   ├── tests
│   │   └── .gitkeep
│   ├── tmp -> /boozo-hub/boozo/data/tmp
│   ├── virtualenvs -> /boozo-hub/virtualmachines/virtualenvs
│   │   └── .gitkeep
│   └── www
│       └── .gitkeep
├── boozo-config
│   ├── boozo.alias.sh
│   ├── boozo.env.sh
│   ├── boozo.export.sh
│   ├── boozo.yml
│   └── .gitkeep
├── boozo-dat
│   ├── aid
│   │   ├── .gitkeep
│   │   └── tfrecords
│   │       └── .gitkeep
│   ├── ant
│   │   └── .gitkeep
│   ├── auth
│   │   └── .gitkeep
│   ├── cfg
│   │   └── .gitkeep
│   ├── cloud
│   │   └── .gitkeep
│   ├── databases
│   │   ├── .gitkeep
│   │   └── mongodb
│   │       ├── configdb
│   │       │   └── .gitkeep
│   │       ├── db
│   │       │   └── .gitkeep
│   │       ├── .gitkeep
│   │       ├── key
│   │       │   └── .gitkeep
│   │       └── logs
│   │           └── .gitkeep
│   ├── docker
│   │   └── .gitkeep
│   ├── downloads
│   │   └── .gitkeep
│   ├── external
│   │   └── .gitkeep
│   ├── kbank
│   │   └── .gitkeep
│   ├── logs
│   │   ├── .gitkeep
│   │   └── www
│   │       └── .gitkeep
│   ├── mnt
│   │   └── .gitkeep
│   ├── mobile
│   │   └── .gitkeep
│   ├── npm-packages
│   │   └── .gitkeep
│   ├── public
│   │   └── .gitkeep
│   ├── public_html
│   │   └── .gitkeep
│   ├── release
│   │   ├── .gitkeep
│   │   ├── keras
│   │   │   └── .gitkeep
│   │   └── torch
│   │       └── .gitkeep
│   ├── reports
│   │   └── .gitkeep
│   ├── samples
│   │   └── .gitkeep
│   ├── _site
│   │   └── .gitkeep
│   ├── team
│   │   ├── .gitkeep
│   │   └── images
│   │       └── .gitkeep
│   ├── tmp
│   │   └── .gitkeep
│   ├── tools
│   │   └── .gitkeep
│   ├── uploads
│   │   └── .gitkeep
│   └── workspaces
│       └── .gitkeep
├── boozo-mobile
│   └── android
│       ├── apps
│       │   └── .gitkeep
│       ├── dist
│       │   └── .gitkeep
│       ├── external
│       │   └── .gitkeep
│       ├── .gitkeep
│       ├── plugins
│       │   └── .gitkeep
│       └── sdk
│           └── .gitkeep
└── virtualmachines
    ├── .gitkeep
    └── virtualenvs
        └── .gitkeep

103 directories, 105 files
```

## Debugging

* Python log level are supported to set the module/package logger settings:
  * `CRITICAL`
  * `ERROR`
  * `WARNING`
  * `INFO`
  * `DEBUG`
  * `NOTSET`
* Export the environment variable to the required log level
  ```bash
  export _PYBOOZO_LOG_LEVEL_='DEBUG'
  ```

## Credit

* Snek logo by [Amir Rachum](https://amir.rachum.com/blog/2017/07/28/python-entry-points/)
* Cli color coding inspired from: [colorama](https://pypi.org/project/colorama/), [termcolor](https://pypi.org/project/termcolor/)
* Cli inputs using [click](https://pypi.org/project/click/)

