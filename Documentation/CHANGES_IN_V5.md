# Changes in V5
We have Made the following changes to MetroAE in v5 as compared to previous versions of MetroAE. All changes are summarised in this document.

## MetroAE operation changes
In v4 and before, MetroAE shipped with 2 modes of operation. The container and git clone. With the new release, we have made things a bit easier for the users. There is a single mode of operation. The metroae container option. This new container will be dynamically built on the users machine. The only pre-requisite for the user will be to have docker installed on their MetroAE Host Machine. The changes for moving from v4 to v5 are as below depending on type of installation. 

### Moving from MetroAE git clone/download to MetroAE v5
1. Download or git pull the latest metroae code
2. Make sure docker is installed and running. The `docker ps` command can verify this. 
3. Use `./metroae-container` instead of `./metroae`. All other arguments remain the same. 
4. For all image paths, make sure they start with `/metroae`. Here `/metroae` refers to the present working directory for the user. 
   e.g. 
   `nuage_unzipped_files_dir: ./images/20.10.R4` changes to `nuage_unzipped_files_dir: /metroae/images/20.10.R4`
5. All the specified paths for licenses, unzipped files, backup directories should be inside the metroae repository. e.g. you cannot specify /opt or /tmp for the metroae host. If your mount directory for images is outside the metroae folder, you can use a mount bind to put them inside the metroae directory. 
   e.g. 
   `sudo mount --bind -o ro /mnt/nfs-data /<your-repo-location>/images`
6. Users do not need to run setup at all, all dependencies will be automatically taken care of with the new container in the background.

### Moving from MetroAE v4 container/download to MetroAE v5
1. Download or git pull the latest metroae code
2. Destroy the old container using `./metroae-container destroy` command
3. Use `./metroae-container` instead of `/metroae`. All other arguments remain the same.
4. For all image paths, make sure they start with `/metroae` instead of `/metroae_data`. Here `/metroae` refers to the present working directory for the user. 
   e.g. 
   `nuage_unzipped_files_dir: /metroae_data/images/20.10.R4` changes to `nuage_unzipped_files_dir: /metroae/images/20.10.R4`
5. You can create a `images` folder in `nuage-metroae` and move the `/metroae_data` mount folder under `/<your-repo-location>/images` athat way you can replace `/metroae_data` with `/metroae_data/images` in the deployment files. 

## Ansible and Python Changes
MetroAE is now supported with Ansible version 3.4.0 and higher. Python3 is now required. Do not worry, the container that gets dynamically created should take care of the python, ansible and any other dependencies that are needed. 

## MetroAE Config
MetroaAE Config is no longer bundled with MetroAE. Please refer to https://github.com/nuagenetworks/nuage-metroae-config to get information on how use MetroAE Config.
