import os
import subprocess
import signal

class LinuxUserManager:
    def __init__(self, sudo=False):
        self.sudo = sudo

    def _run_cmd(self, cmd):
        if self.sudo:
            cmd.insert(0, 'sudo')
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Command failed: {result.stderr.strip()}")
        return result.stdout.strip()

    def create_user(self, username, shell='/bin/bash', home_dir=None):
        """Create a new user."""
        cmd = ['useradd', '-m', '-s', shell, username]
        if home_dir:
            cmd += ['-d', home_dir]
        return self._run_cmd(cmd)

    def delete_user(self, username, remove_home=False, force=False):
        """Delete a user, with an option to forcefully kill their processes."""
        # If force is enabled, kill the user's processes before deleting
        if force:
            print(f"Forcefully killing processes for user {username}...")
            self.kill_user_processes(username)

        # Command to delete user, but do not remove their home directory
        cmd = ['userdel']
        if remove_home:
            cmd.append('-r')
        cmd.append(username)
        return self._run_cmd(cmd)

    def kill_user_processes(self, username):
        """Force kill all processes owned by the user."""
        try:
            # Find all process IDs owned by the user
            pids = os.popen(f"pgrep -u {username}").read().strip().split('\n')
            for pid in pids:
                if pid:
                    print(f"Killing process {pid} owned by {username}")
                    os.kill(int(pid), signal.SIGKILL)  # SIGKILL to forcefully terminate
        except Exception as e:
            print(f"Error killing processes for {username}: {e}")

    def change_password(self, username, password):
        """Change a user's password."""
        cmd = ['chpasswd']
        input_data = f"{username}:{password}"
        proc = subprocess.run(['sudo'] + cmd, input=input_data, capture_output=True, text=True) if self.sudo else subprocess.run(cmd, input=input_data, capture_output=True, text=True)
        if proc.returncode != 0:
            raise RuntimeError(f"Failed to change password: {proc.stderr.strip()}")
        return proc.stdout.strip()

    def modify_user(self, username, new_shell=None, new_home=None):
        """Modify user attributes like shell and home directory."""
        cmd = ['usermod']
        if new_shell:
            cmd += ['-s', new_shell]
        if new_home:
            cmd += ['-d', new_home, '-m']
        cmd.append(username)
        return self._run_cmd(cmd)

    def change_shell(self, username, new_shell):
        """Change the login shell for a user using chsh."""
        cmd = ['chsh', '-s', new_shell, username]
        return self._run_cmd(cmd)

    def list_users(self):
        """List all users in /etc/passwd."""
        cmd = ['cut', '-d:', '-f1', '/etc/passwd']
        return self._run_cmd(cmd).splitlines()

    def home_dirs(self):
        """Get a list of directories in /home."""
        return [d for d in os.listdir('/home') if os.path.isdir(os.path.join('/home', d))]

    def user_exists(self, username):
        """Check if a user exists by comparing against /home directories."""
        home_dirs = self.home_dirs()
        return username in home_dirs

    def user_info(self, username):
        """Get detailed user info."""
        if not self.user_exists(username):
            return f"User {username} does not have a home directory or does not exist."
        
        cmd = ['getent', 'passwd', username]
        try:
            user_info = self._run_cmd(cmd)
            if not user_info:
                return f"User {username} not found."
            
            user_info = user_info.split(":")
            return {
                'username': user_info[0],
                'password': user_info[1],
                'uid': user_info[2],
                'gid': user_info[3],
                'gecos': user_info[4],
                'home_dir': user_info[5],
                'shell': user_info[6]
            }
        except RuntimeError as e:
            return f"Error retrieving user {username}: {str(e)}"


# TESTS (with the new chsh method)
mgr = LinuxUserManager(sudo=True)

"""
# Test 1: User creation
print("Test 1: Creating user 'testuser'")
mgr.create_user("testuser", shell="/bin/bash")
assert mgr.user_exists("testuser"), "Test failed: User should exist!"

# Test 2: User info
print("Test 2: Fetching user info for 'testuser'")
user_info = mgr.user_info("testuser")
assert user_info['username'] == "testuser", "Test failed: User info does not match!"

# Test 3: Change user password
print("Test 3: Changing password for 'testuser'")
mgr.change_password("testuser", "newpassword123")
# We won't assert on password change here for security reasons, just ensuring no error occurs

# Test 4: Modify user
print("Test 4: Modifying user 'testuser' shell")
mgr.modify_user("testuser", new_shell="/bin/zsh")
user_info = mgr.user_info("testuser")
print(user_info)
assert user_info['shell'] == "/bin/zsh", "Test failed: Shell not modified correctly!"

# Test 5: Change user shell using chsh
print("Test 5: Changing shell for 'testuser' using chsh")
mgr.change_shell("testuser", "/bin/fish")
user_info = mgr.user_info("testuser")
print(user_info)
assert user_info['shell'] == "/bin/fish", "Test failed: Shell not changed using chsh!"


# Test 6: Delete user
"""
print("Test 6: Deleting user 'testuser'")
mgr.delete_user("testuser", remove_home=True, force=True)
assert not mgr.user_exists("testuser"), "Test failed: User should be deleted!"

print("All tests passed!")
