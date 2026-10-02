
import os

class Annotator:
    def __init__(self, prefix="BFG_"):
        self.prefix = prefix
        self.counter = 0

# orfs لیست هاست. لیستی از آبجکت ها
    def annotate(self, orfs):
        annotated_orfs = []

        for orf in orfs:
            self.counter += 1

            orf_id = self.prefix + str(self.counter).zfill(3)

            annotation = {
                "id": orf_id,
                "strand": orf.strand,
                "frame": orf.frame,
                "pos_start": orf.pos_start,
                "protein": orf.protein,
                "is_complete": orf.is_complete,
                "motifs": orf.motifs,
                "molecular_weight": orf.molecular_weight
            }

            annotated_orfs.append(annotation)

        return annotated_orfs


def write_report(annotated_orfs, output_path):

    directory = os.path.dirname(output_path)

    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        for orf in annotated_orfs:

            if orf["is_complete"]:
                status = "Complete"
            else:
                status = "Incomplete"

            file.write("ID: " + orf["id"] + "\n")
            file.write("Strand: " + str(orf["strand"]) + "\n")
            file.write("Frame: " + str(orf["frame"]) + "\n")
            file.write(
                "Start Position: "
                + str(orf["pos_start"]) + "\n"
            )
            file.write("Protein: " + orf["protein"] + "\n")
            file.write("Status: " + status + "\n")

            weight = orf["molecular_weight"]

            file.write(
                "Molecular Weight: "
                + str(weight) + "\n"
            )

            file.write("Motifs:\n")

            for motif in orf["motifs"]:
                file.write(
                    "  "
                    + motif["sequence"]
                    + " at position "
                    + str(motif["position"])
                    + "\n"
                )

            file.write("-" * 40 + "\n")

    print("Report saved to:", output_path)