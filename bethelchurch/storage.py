from storages.backends.s3 import S3Storage

class SupabaseMediaStorage(S3Storage):
    def url(self, name, parameters=None, expire=None, http_method=None):
        return (
            f"https://fenyxjqtnczwqrrehgpb.supabase.co"
            f"/storage/v1/object/public/{self.bucket_name}/{name}"
        )