import os
import shutil

def get_linux_productname():
    print("Getting Linux product name in order to apply quirks...", end='')
    with open("/sys/class/dmi/id/product_name") as f:
        product_name = f.read().strip()
    print(product_name)
    return product_name

def crosvm_quirks():
    print("Applying Chrome OS crostini quirks...")
    os.environ["QT_QPA_PLATFORM"] = "xcb"

def copy_if_not_exists(src, dst, *, follow_symlinks=True):
    if not os.path.exists(dst):
        print(f"{dst} does not exist, copying...")
        return shutil.copy2(src, dst, follow_symlinks=follow_symlinks)
    else:
        print(f"{dst} already exists, not copying...")
