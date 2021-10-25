# Standard library imports
import os

# Third party imports
import fitz

# Local application imports


class ImportInvoices:
    def __init__(self, uploaded_files, company_id):
        self.uploaded_files = uploaded_files
        self.company_id = company_id

        self.make_dirs()
        self.thumbnails = self.make_thumbnails()
        self.file_paths = self.save_files()

    @property
    def filenames(self) ->list:
        return list(map(lambda x: x.filename, self.uploaded_files))

    def make_thumbnails(self) -> list:
        thumbnails = []
        for uploaded_file in self.uploaded_files:

            root_filename, ext_filename = os.path.splitext(uploaded_file.filename)

            if ext_filename.lower() == ".pdf":

                doc = fitz.open(filename=uploaded_file.filename,
                                stream=uploaded_file.stream.read(),
                                filetype=uploaded_file.content_type)

                page = doc.loadPage(0)
                pix = page.getPixmap(matrix=fitz.Matrix(150/72,150/72))

                output_path = os.path.join("allocate",
                                           "uploads",
                                           str(self.company_id),
                                           "thumbnails",
                                           root_filename+".png")
                pix.writePNG(output_path)

            else:
                output_path = os.path.join("allocate",
                                           "uploads",
                                            str(self.company_id),
                                           "thumbnails",
                                            uploaded_file.filename)
                uploaded_file.save(output_path)

            thumbnails.append(output_path)
        return thumbnails

    def save_files(self):
        file_paths = []
        for uploaded_file in self.uploaded_files:
            output_path = os.path.join("allocate",
                                       "uploads",
                                       str(self.company_id),
                                       "invoices",
                                       uploaded_file.filename)
            uploaded_file.stream.seek(0)
            uploaded_file.save(output_path)
            file_paths.append(output_path)
        return file_paths

    def make_dirs(self):

        thumbnail_path = os.path.join("allocate","uploads", str(self.company_id),"thumbnails")
        invoice_path = os.path.join("allocate","uploads",str(self.company_id),"invoices")
        stamped_path = os.path.join("allocate","uploads",str(self.company_id), "stamped")

        if not os.path.exists(thumbnail_path):
            os.makedirs(thumbnail_path)

        if not os.path.exists(invoice_path):
            os.makedirs(invoice_path)

        if not os.path.exists(stamped_path):
            os.makedirs(stamped_path)
