#!/usr/bin/env python3
"""
Simple File Permission Analyzer
Easy-to-understand code for checking file permissions.
"""

import os
import stat
import datetime

# Try to get user/group names (works on Mac/Linux)
try:
    import pwd
    import grp
    CAN_GET_NAMES = True
except:
    CAN_GET_NAMES = False


def check_file(file_path):
    """Check file permissions - main function."""
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"\n❌ File not found: {file_path}")
        return
    
    # Get file info
    info = os.stat(file_path)
    mode = info.st_mode
    
    # Show header
    print("\n" + "="*60)
    print(f"📁 File: {file_path}")
    print("="*60)
    
    # Basic info
    print(f"\n📋 Type: {'Directory' if os.path.isdir(file_path) else 'File'}")
    print(f"💾 Size: {info.st_size} bytes")
    
    # Owner info
    print(f"\n👤 Owner ID: {info.st_uid}")
    print(f"👥 Group ID: {info.st_gid}")
    
    if CAN_GET_NAMES:
        try:
            owner_name = pwd.getpwuid(info.st_uid).pw_name
            group_name = grp.getgrgid(info.st_gid).gr_name
            print(f"   Owner: {owner_name}")
            print(f"   Group: {group_name}")
        except:
            pass
    
    # Permissions
    print(f"\n🔐 Permissions: {stat.filemode(mode)} ({oct(stat.S_IMODE(mode))})")
    print("-"*60)
    
    # Owner permissions
    can_read = bool(mode & stat.S_IRUSR)
    can_write = bool(mode & stat.S_IWUSR)
    can_execute = bool(mode & stat.S_IXUSR)
    print(f"Owner:   {'r' if can_read else '-'}{'w' if can_write else '-'}{'x' if can_execute else '-'}")
    
    # Group permissions
    can_read = bool(mode & stat.S_IRGRP)
    can_write = bool(mode & stat.S_IWGRP)
    can_execute = bool(mode & stat.S_IXGRP)
    print(f"Group:   {'r' if can_read else '-'}{'w' if can_write else '-'}{'x' if can_execute else '-'}")
    
    # Others permissions
    can_read = bool(mode & stat.S_IROTH)
    can_write = bool(mode & stat.S_IWOTH)
    can_execute = bool(mode & stat.S_IXOTH)
    print(f"Others:  {'r' if can_read else '-'}{'w' if can_write else '-'}{'x' if can_execute else '-'}")
    
    # Special permissions
    has_setuid = bool(mode & stat.S_ISUID)
    has_setgid = bool(mode & stat.S_ISGID)
    has_sticky = bool(mode & stat.S_ISVTX)
    
    if has_setuid or has_setgid or has_sticky:
        print(f"\n⭐ Special:")
        if has_setuid:
            print("   • Setuid (runs as owner)")
        if has_setgid:
            print("   • Setgid (runs as group)")
        if has_sticky:
            print("   • Sticky bit (protected delete)")
    
    # Security warnings
    print(f"\n🛡️  Security Check:")
    warnings = []
    
    if mode & stat.S_IWOTH:
        warnings.append("⚠️  Anyone can modify this!")
    if mode & stat.S_ISUID:
        warnings.append("⚠️  Runs with special privileges")
    if os.path.isdir(file_path) and (mode & stat.S_IWOTH) and not (mode & stat.S_ISVTX):
        warnings.append("⚠️  Unsafe directory permissions!")
    
    if warnings:
        for w in warnings:
            print(f"   {w}")
    else:
        print("   ✅ No issues found")
    
    # Timestamps
    modified = datetime.datetime.fromtimestamp(info.st_mtime)
    print(f"\n📅 Last modified: {modified.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")


if __name__ == "__main__":
    import sys
    
    # Get file path from command line or use current directory
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = "."
    
    check_file(file_path)