sudo qemu-system-i386 --device e1000,netdev=enp0s3,mac=aa:bb:cc:dd:ee:ff \
	--netdev tap,id=enp0s3,script=custom-scripts/qemu-ifup \
	--kernel output/images/bzImage \
	--hda output/images/rootfs.ext2 \
	--nographic \
	--append "console=ttyS0 root=/dev/sda" 
