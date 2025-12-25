import os
import uuid

from fastapi import HTTPException, UploadFile

# Define allowed extensions and max file size (5 MB)
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024

# FileHandler class to manage file operations
class FileHandler:
    @staticmethod
    # Validate uploaded image file
    def validate_image(file: UploadFile) -> None:
        if file.filename is None:
            raise HTTPException(
                status_code=400,
                detail="No filename provided"
            )
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
            )
        
    @staticmethod
    # Save uploaded file and return its URL path
    async def save_upload_file(file: UploadFile, upload_dir: str) -> str:
        FileHandler.validate_image(file)
        if file.filename is None:
            raise HTTPException(
                status_code=400,
                detail="No filename provided"
            )
        file_ext = os.path.splitext(file.filename)[1].lower()
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(upload_dir, unique_filename)

        try:
            contents = await file.read()

            if len(contents) > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=400,
                    detail=f"File size exceeds the maximum limit of {MAX_FILE_SIZE // (1024 * 1024)} MB.",
                )
            with open(file_path, "wb") as f:
                f.write(contents)

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                 detail=f"Failed to save file: {str(e)}",
            )
        finally:
            await file.close()
        url_path = file_path.replace("app","",1)
        return url_path
    
    @staticmethod
    # Delete file by its URL path
    def delete_file(file_url: str) -> bool:
        file_path = f"app{file_url}" 

        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            else:
                return False
        except Exception:
            return False
