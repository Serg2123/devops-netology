1. "разряженные" файлы в которых 0 заменяются последовательностью нулей, эффективно для экономии места образов и ФС ОС которые развернуты, но не загружены данными. 
2. нет, т.к. жесткая ссылка и файл, для которой она создана, имеют одинаковые inode, соотвественно жесткая ссылка имеет те же права доступа, владельца и время последней модификации, что и целевой файл.  
3.  
Далее все под root-ом:  
4.  fdisk-ом в интерактивном режиме с командой n создали primary раздел от начала до +2GB, второй primary раздел от начала свободного места до конца диска.  
5.  sfdisk -d /dev/sdb > sdb_part.txt  
    sfdisk /dev/sdc < sdb_part.txt  
6.  mdadm --create --verbose /dev/md0 -l 1 -n 2 /dev/sdb1 /dev/sdc1   # (Raid 1)  
7.  mdadm --create --verbose /dev/md1 -l 0 -n 2 /dev/sdb2 /dev/sdc2   # (Raid 0)  
8.  pvcreate /dev/md{0,1}  
9.  vgcreate vol_grp_from_raid /dev/md{0,1}  
10.  lvcreate -L 100M -n log_volm01 vol_grp_from_raid /dev/md1  
11.  mkfs.ext4 /dev/vol_grp_from_raid/log_volm01  
12. cd /  
    mkdir /tmp/new  
    mount /dev/vol_grp_from_raid/log_volm01 /tmp/new  
13.  
14. root@vagrant:/tmp/new# lsblk  
NAME                               MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT  
sda                                  8:0    0   64G  0 disk  
├─sda1                               8:1    0  512M  0 part  /boot/efi  
├─sda2                               8:2    0    1K  0 part  
└─sda5                               8:5    0 63.5G  0 part  
  ├─vgvagrant-root                 253:0    0 62.6G  0 lvm   /  
  └─vgvagrant-swap_1               253:1    0  980M  0 lvm   [SWAP]  
sdb                                  8:16   0  2.5G  0 disk  
├─sdb1                               8:17   0    2G  0 part  
│ └─md0                              9:0    0    2G  0 raid1  
└─sdb2                               8:18   0  511M  0 part  
  └─md1                              9:1    0 1018M  0 raid0  
    └─vol_grp_from_raid-log_volm01 253:2    0  100M  0 lvm   /tmp/new  
sdc                                  8:32   0  2.5G  0 disk  
├─sdc1                               8:33   0    2G  0 part  
│ └─md0                              9:0    0    2G  0 raid1  
└─sdc2                               8:34   0  511M  0 part  
  └─md1                              9:1    0 1018M  0 raid0  
    └─vol_grp_from_raid-log_volm01 253:2    0  100M  0 lvm   /tmp/new  
15. 
root@vagrant:/tmp/new# gzip -t /tmp/new/test.gz  
root@vagrant:/tmp/new# echo $?  
0  

16. 
root@vagrant:/# pvmove -v -n log_volm01 /dev/md1 /dev/md0  
  Archiving volume group "vol_grp_from_raid" metadata (seqno 6).  
  Creating logical volume pvmove0  
  activation/volume_list configuration setting not defined: Checking only host tags for vol_grp_from_raid/log_volm01.  
  Moving 25 extents of logical volume vol_grp_from_raid/log_volm01.  
  activation/volume_list configuration setting not defined: Checking only host tags for vol_grp_from_raid/log_volm01.  
  Creating vol_grp_from_raid-pvmove0  
  Loading table for vol_grp_from_raid-pvmove0 (253:3).  
  Loading table for vol_grp_from_raid-log_volm01 (253:2).  
  Suspending vol_grp_from_raid-log_volm01 (253:2) with device flush  
  Resuming vol_grp_from_raid-pvmove0 (253:3).  
  Resuming vol_grp_from_raid-log_volm01 (253:2).  
  Creating volume group backup "/etc/lvm/backup/vol_grp_from_raid" (seqno 7).  
  activation/volume_list configuration setting not defined: Checking only host tags for vol_grp_from_raid/pvmove0.  
  Checking progress before waiting every 15 seconds.  
  /dev/md1: Moved: 12.00%  
  /dev/md1: Moved: 100.00%  
  Polling finished successfully.  

root@vagrant:/# lsblk  
NAME                               MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT  
sda                                  8:0    0   64G  0 disk  
├─sda1                               8:1    0  512M  0 part  /boot/efi  
├─sda2                               8:2    0    1K  0 part  
└─sda5                               8:5    0 63.5G  0 part  
  ├─vgvagrant-root                 253:0    0 62.6G  0 lvm   /  
  └─vgvagrant-swap_1               253:1    0  980M  0 lvm   [SWAP]  
sdb                                  8:16   0  2.5G  0 disk  
├─sdb1                               8:17   0    2G  0 part  
│ └─md0                              9:0    0    2G  0 raid1  
│   └─vol_grp_from_raid-log_volm01 253:2    0  100M  0 lvm   /tmp/new  
└─sdb2                               8:18   0  511M  0 part  
  └─md1                              9:1    0 1018M  0 raid0  
sdc                                  8:32   0  2.5G  0 disk  
├─sdc1                               8:33   0    2G  0 part  
│ └─md0                              9:0    0    2G  0 raid1  
│   └─vol_grp_from_raid-log_volm01 253:2    0  100M  0 lvm   /tmp/new  
└─sdc2                               8:34   0  511M  0 part  
  └─md1                              9:1    0 1018M  0 raid0  

17.  mdadm /dev/md0 --fail /dev/sdc1  

18.  
[Tue Sep 28 15:44:06 2021] md/raid1:md0: Disk failure on sdc1, disabling device.  
                           md/raid1:md0: Operation continuing on 1 devices.  
root@vagrant:/# mdadm -D /dev/md0  
/dev/md0:  
           Version : 1.2  
     Creation Time : Mon Sep 27 22:20:37 2021  
        Raid Level : raid1  
        Array Size : 2094080 (2045.00 MiB 2144.34 MB)  
     Used Dev Size : 2094080 (2045.00 MiB 2144.34 MB)  
      Raid Devices : 2  
     Total Devices : 2  
       Persistence : Superblock is persistent  

       Update Time : Tue Sep 28 15:44:08 2021  
             State : clean, degraded  
    Active Devices : 1  
   Working Devices : 1  
    Failed Devices : 1  
     Spare Devices : 0  

Consistency Policy : resync  

              Name : vagrant:0  (local to host vagrant)  
              UUID : 97c62a74:01016c29:68b235af:6422c24a  
            Events : 19  

    Number   Major   Minor   RaidDevice State  
       0       8       17        0      active sync   /dev/sdb1  
       -       0        0        1      removed  
       1       8       33        -      faulty   /dev/sdc1  

19.  
root@vagrant:/# gzip -t /tmp/new/test.gz  
root@vagrant:/# echo $?  
0  
