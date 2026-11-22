import hashlib
import sys
from datetime import date
from http.client import HTTPException
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen


COMMIT = "382ee6c662b0ece26e111f263b44c029afad7787"
FILES = (
    "owid-co2-data.csv",
    "owid-co2-codebook.csv",
)
CHUNK_SIZE = 1024 * 1024


class DownloadError(Exception):
    pass


def download_file(url: str, destination: Path) -> bool:
    try:
        output = destination.open("xb")
    except FileExistsError:
        return False
    except OSError as exc:
        raise DownloadError(f"cannot create {destination}: {exc}") from exc

    try:
        with output, urlopen(url) as response:
            while chunk := response.read(CHUNK_SIZE):
                output.write(chunk)
    except (HTTPException, OSError, URLError) as exc:
        try:
            destination.unlink()
        except OSError as cleanup_error:
            raise DownloadError(
                f"download failed for {destination.name}: {exc}; "
                f"could not remove incomplete file: {cleanup_error}"
            ) from cleanup_error
        raise DownloadError(f"download failed for {destination.name}: {exc}") from exc

    return True


def file_details(path: Path) -> tuple[int, str]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as source:
        while chunk := source.read(CHUNK_SIZE):
            size += len(chunk)
            digest.update(chunk)
    return size, digest.hexdigest()


def main() -> int:
    raw_dir = Path(__file__).resolve().parents[1] / "data" / "raw"

    for filename in FILES:
        url = (
            f"https://raw.githubusercontent.com/owid/co2-data/"
            f"{COMMIT}/{filename}"
        )
        destination = raw_dir / filename
        try:
            downloaded = download_file(url, destination)
        except DownloadError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1

        if downloaded:
            sources_path = raw_dir / "SOURCES.txt"
            try:
                with sources_path.open("a", encoding="utf-8") as sources:
                    sources.write(
                        f"{date.today().isoformat()}\t{url}\t{filename}\n"
                    )
            except OSError as exc:
                print(
                    f"Error: cannot append to {sources_path}: {exc}",
                    file=sys.stderr,
                )
                return 1

    for filename in FILES:
        path = raw_dir / filename
        try:
            size, checksum = file_details(path)
        except OSError as exc:
            print(f"Error: cannot read {path}: {exc}", file=sys.stderr)
            return 1
        print(f"{filename}: {size} bytes, SHA-256 {checksum}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
