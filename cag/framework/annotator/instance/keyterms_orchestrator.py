from pyArango.document import Document
from cag.framework.annotator.element.orchestrator import PipeOrchestrator
import pandas as pd


class KeyTermsPipeOrchestrator(PipeOrchestrator):
    def create_node(self, term) -> Document:
        data = {"term": term}
        return self.upsert_node(self.node_name,
                                data,
                                alt_key=["term"])

    def create_edge(self, from_: Document, to_: Document, entry) -> Document:
        return self.upsert_edge(self.edge_name, from_, to_, edge_attrs=entry)

    def save_annotations(self, annotated_texts: "[]"):
        out_arr = []
        for doc, context in annotated_texts:
            text_key = context["_key"]

            for rank, (term, score) in doc._.keyterms:
                
                keyterm_node: Document = self.create_node(term)
                text_node: Document = self.get_document(
                    self.annotated_node, {"_key": text_key}
                )

                entry = {
                    "rank": rank,
                    "score": score
                }

                _: Document = self.create_edge(
                    text_node, keyterm_node, entry
                )

                record = {f"metodeo_keyterm_{x}": y for x, y in entry.items()}
                record["metodeo_keyterm"] = term
                out_arr.append(record)
        out_df: pd.DataFrame = pd.DataFrame(out_arr)

        return out_df
