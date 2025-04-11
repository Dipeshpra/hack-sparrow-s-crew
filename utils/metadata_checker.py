import subprocess

def check_metadata(filepath):
    try:
        result = subprocess.check_output([
            'ffprobe', '-v', 'error', '-show_entries',
            'format_tags', '-of', 'default=noprint_wrappers=1:nokey=0',
            filepath
        ])
        decoded = result.decode('utf-8').strip()
        if not decoded:
            return "No significant metadata found. This might indicate tampering or stripping."
        return decoded
    except Exception as e:
        return f"Error retrieving metadata: {str(e)}"
