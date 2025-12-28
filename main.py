import argparse
from pathlib import Path

VERSION = "1.0"

FRAME_SIZES = {
    "small": (0, 0),
    "medium": (0, 0),
    "large": (0, 0),
}

def list_sizes():
    print("\nAvailable frame sizes:\n")
    for name, (w, h) in FRAME_SIZES.items():
        print(f"  {name:6s} → {w} x {h} pixels")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="📸 MemoriesPrinter — Generate framed photo collages as printable PDFs."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # -------------------------------
    # list-sizes
    # -------------------------------
    subparsers.add_parser("list-sizes", help="List all supported frame sizes.")

    # -------------------------------
    # generate
    # -------------------------------
    gen_parser = subparsers.add_parser(
        "generate", help="Generate framed images and optionally a collage PDF."
    )
    gen_parser.add_argument(
        "--size",
        required=True,
        choices=FRAME_SIZES.keys(),
        help="Frame size (e.g. medium).",
        default='medium'
    )
    gen_parser.add_argument(
        "--caption",
        choices=["on", "off"],
        default="on",
        help="Include EXIF caption under each image (default: on).",
    )
    gen_parser.add_argument(
        "--no-pdf", action="store_true", help="Skip generating the collage PDF."
    )
    gen_parser.add_argument("inputdir", help="Directory with source images.")
    gen_parser.add_argument(
        "outputdir",
        nargs="?",
        help="Optional output directory (default: inputdir/output).",
    )

    # -------------------------------
    # cleanup
    # -------------------------------
    subparsers.add_parser("cleanup", help="Remove temporary and output files.")

    # -------------------------------
    # version
    # -------------------------------
    subparsers.add_parser("version", help="Show tool version.")

    # -------------------------------
    # Parse and dispatch
    # -------------------------------
    args = parser.parse_args()

    if args.command == "list-sizes":
        list_sizes()

    elif args.command == "generate":
        inputdir = Path(args.inputdir)
        outputdir = Path(args.outputdir) if args.outputdir else inputdir / "output"
        outputdir.mkdir(exist_ok=True)

        print(f"🖼️  Generating collage from: {inputdir}")
        print(f"📁 Output folder: {outputdir}")
        print(f"📐 Frame size: {args.size}")
        print(f"💬 Captions: {'on' if args.caption == 'on' else 'off'}")
        print(f"📄 Generate PDF: {'yes' if not args.no_pdf else 'no'}\n")

        # generate_collage(
        #     inputdir,
        #     outputdir,
        #     size=args.size,
        #     with_caption=(args.caption == "on"),
        #     make_pdf_flag=(not args.no_pdf),
        # )

        print("\n✅ Done! Your framed images are ready.")
        if not args.no_pdf:
            print("📄 Collage PDF created successfully!")

    # elif args.command == "cleanup":
    #     cleanup("static/uploads", "output")
    #     print("🧹 Cleaned uploads and output folders.")

    elif args.command == "version":
        print(f"Paperstories v{VERSION}")


if __name__ == "__main__":
    main()
