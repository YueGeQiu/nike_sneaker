# -*- coding: utf-8 -*-

from nike_sneaker.nikesnkrs import NikeSNKRS


if __name__ == '__main__':
    banner = """
     ____  _   _ _  ______  ____
    / ___|| \ | | |/ /  _ \/ ___|
    \___ \|  \| | ' /| |_) \____\\
     ___) | |\  | . \|  _ < ___) |
    |____/|_| \_|_|\_\_| \_\____/
    """
    print(banner)
    nike_snkrs = NikeSNKRS()
    nike_snkrs.check_new_release()