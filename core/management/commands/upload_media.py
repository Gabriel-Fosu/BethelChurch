from pathlib import Path
from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from bethelchurch.storage import SupabaseMediaStorage

class Command(BaseCommand):
    help = "Upload all files from the local media folder to Supabase Storage"

    def handle(self, *args, **options):
        media_root = Path(settings.BASE_DIR) / "media"

        if not media_root.exists():
            self.stdout.write(
                self.style.ERROR(f"Media folder not found: {media_root}")
            )
            return

        storage = SupabaseMediaStorage()

        files = [
            file
            for file in media_root.rglob("*")
            if file.is_file()
        ]

        if not files:
            self.stdout.write(
                self.style.WARNING("No files found in the media folder")
            )
            return

        self.stdout.write(f"Found {len(files)} file(s) in the media folder to upload.\n")

        uploaded = 0
        skipped = 0
        failed = 0

        for file_path in files:
            relative_path = file_path.relative_to(media_root)
            storage_name = relative_path.as_posix()

            try:
                if storage.exists(storage_name):
                    self.stdout.write(
                        self.style.WARNING(f"File {storage_name} already exists")
                    )
                    skipped += 1
                    continue

                with file_path.open(mode="rb") as file:
                    storage.save(storage_name, File(file))

                self.stdout.write(
                    self.style.SUCCESS(f"UPLOADED: {storage_name}")
                )
                uploaded += 1

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"FAILED: {storage_name} -> {e}")
                )
                failed += 1

        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(
            self.style.SUCCESS(f"Uploaded {uploaded} file(s).")
        )
        self.stdout.write(
            self.style.WARNING(f"Skipped {skipped} file(s).")
        )
        self.stdout.write(
            self.style.ERROR(f"Failed {failed} file(s).")
        )
        self.stdout.write("=" * 50)