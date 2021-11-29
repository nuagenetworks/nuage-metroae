#!/usr/bin/env bash
echo "NESC OPENSTACK - METROAE"
source nesc-openstack-source.sh
status=$?

if [[ $status -ne 0 ]]; then
        echo "Setting default MetroAE NESC OpenStack authencation failure."
        exit 1
else
    echo "Successfully added authencation. Check it."
    env | grep OS_
fi

echo ""
echo ""
nova list
status=$?
echo ""
echo "******************************************************END OF THE LIST*****************************************************"

if [[ $status -ne 0 ]]; then
    echo "Error to list down instanses from OpenStack"
    exit 1
fi
echo "Check the list of instances and select."

read -p "Enter instance name:" nesc_instance

openstack server stop $nesc_instance
status=$?

if [[ $status -ne 0 ]]; then
    echo "Failed to stop $nesc_instance. May be that instance is not valid."
    exit 1
fi

echo ""
echo ""
nova list | grep $nesc_instance
status=$?
echo ""

if [[ $status -ne 0 ]]; then
    echo "Error to list down instanse infromation from OpenStack"
    exit 1
fi

read -p "Enter snapshot name:" nesc_instance_snap

openstack server image create --name $nesc_instance_snap $nesc_instance

status=$?
if [[ $status -ne 0 ]]; then
    echo "Error to create snapshot."
    exit 1
fi

openstack image list
status=$?
if [[ $status -ne 0 ]]; then
    echo "Error to list down images from OpenStack"
    exit 1
fi
echo ""
echo "****END OF THE LIST****"
echo ""
echo "Newly created image information"

openstack image list | grep $nesc_instance_snap
status=$?
if [[ $status -ne 0 ]]; then
    echo "Error to list down images from OpenStack"
    exit 1
fi

echo ""
echo "*****DOWNLOAD SNAPSHOT*****"

user_choice="init"
while [[ $user_choice != "y" ]] && [[ $user_choice != "n" ]] && [[ $user_choice != "" ]]
do
    read -p "Do you want to download the snapshot?(y/n)" user_choice
done

if [[ $user_choice -eq "y" ]]; then
    read -p "Enter image ID of snapshot: " nesc_snapshot_id
    openstack image save --file snapshot.raw $nesc_snapshot_id
    status=$?
    if [[ $status -ne 0 ]]; then
        echo "Error to download images from OpenStack"
        exit 1
    fi
else
    echo "You have to download snapshot image to import it into new environment."
    echo ""
fi

openstack flavor list
status=$?
if [[ $status -ne 0 ]]; then
    echo "Error to list down flavors from OpenStack"
    exit 1
fi
read -p "Select snapshot flavor:" nesc_snapshot_flavor

openstack network list
status=$?
if [[ $status -ne 0 ]]; then
    echo "Error to list down network IDs from OpenStack"
    exit 1
fi
read -p "Select network id:" nesc_openstack_net_id
echo ""
echo ""
read -p "Enter new name for new instance: " nesc_snap_new_instance

nova boot --flavor $nesc_snapshot_flavor --nic net-id=$nesc_openstack_net_id --image $nesc_instance_snap $nesc_snap_new_instance
status=$?
if [[ $status -ne 0 ]]; then
    echo "Error to boot new instance from the snapshot"
    exit 1
fi

echo ""
echo "*****STATUS OF INSTANCE AND SNAPSHOT*****"
echo "________________________________________________________________________________________________________"
nova list | grep $nesc_instance
echo ""
echo "________________________________________________________________________________________________________"
nova list | grep $nesc_snap_new_instance
echo ""
echo "________________________________________________________________________________________________________"
openstack image list | grep $nesc_instance_snap