import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Header (Only on page 2 onwards)
        if self._pageNumber > 1:
            self.drawString(36, 810, "BioDB Internal & Quiz Master Preparation Guide | Modules 1, 3, 4, 5, 6")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(36, 804, 559, 804)
        
        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(559, 25, page_text)
        self.drawString(36, 25, "Confidential - Prepared for Lab Internal & Theory Examination")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(36, 35, 559, 35)
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()

    # Custom styles
    c_primary = colors.HexColor("#1A365D")   # Deep Navy
    c_secondary = colors.HexColor("#2B6CB0") # Medium Blue
    c_accent = colors.HexColor("#C53030")    # Crimson Red
    c_dark = colors.HexColor("#2D3748")      # Charcoal Text
    c_bg_light = colors.HexColor("#F7FAFC")  # Light gray-blue
    c_callout = colors.HexColor("#EDF2F7")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=c_primary,
        alignment=1, # Center
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#4A5568"),
        alignment=1,
        spaceAfter=15
    )

    part_header_style = ParagraphStyle(
        'PartHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=colors.white,
        spaceBefore=0,
        spaceAfter=0,
        alignment=0
    )

    h1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13.5,
        textColor=c_secondary,
        spaceBefore=9,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=c_dark,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=c_dark,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'CustomCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#1A202C")
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=c_dark
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=c_primary
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    callout_text = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#2C5282")
    )

    story = []

    def make_banner(text, bg_color=c_primary):
        p = Paragraph(f"<b>{text}</b>", part_header_style)
        t = Table([[p]], colWidths=[523])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), bg_color),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        return t

    def make_code_box(code_text):
        p = Paragraph(code_text.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style)
        t = Table([[p]], colWidths=[523])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EDF2F7")),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        return t

    def make_callout(text, prefix="IMPORTANT EXAM TIP: "):
        full_text = f"<b>{prefix}</b>{text}"
        p = Paragraph(full_text, callout_text)
        t = Table([[p]], colWidths=[523])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EBF8FF")),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#bee3f8")),
            ('LINELEFT', (0, 0), (0, -1), 3, colors.HexColor("#3182CE")),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        return t

    # -------------------------------------------------------------
    # TITLE & METADATA
    # -------------------------------------------------------------
    story.append(Paragraph("BIOLOGICAL DATABASES (BioDB)", title_style))
    story.append(Paragraph("<b>Comprehensive Lab Internal & Quiz Master Preparation Handbook</b><br/>Covers Modules 1, 3, 4, 5, 6 | In-depth Theory + Step-by-Step Practical Protocols", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=0, spaceAfter=10))

    # Executive Syllabus Map Table
    syl_data = [
        [Paragraph("Module", table_header), Paragraph("Focus Areas & Topics Covered", table_header), Paragraph("Practical / Lab Skills", table_header)],
        [
            Paragraph("<b>Mod 1: Sequence Submission</b>", table_cell_bold),
            Paragraph("Central dogma, RDBMS, BankIt, Webin, SAKURA, FASTA, GenBank, EMBL, ReadSeq.", table_cell),
            Paragraph("File format syntax, header parsing, sequence format conversion via ReadSeq/seqret.", table_cell)
        ],
        [
            Paragraph("<b>Mod 3: Seq Databases</b>", table_cell_bold),
            Paragraph("INSDC (GenBank, EMBL-EBI, DDBJ), UniProt (Swiss-Prot vs TrEMBL), PIR, COSMIC, ClinVar, dbSNP.", table_cell),
            Paragraph("RefSeq vs GenBank IDs, rsID querying, filtering clinically significant variants.", table_cell)
        ],
        [
            Paragraph("<b>Mod 4: Structure DBs</b>", table_cell_bold),
            Paragraph("PDB, mmCIF, coordinate records, SCOP (C-F-S-F), CATH (C-A-T-H).", table_cell),
            Paragraph("PDB header parsing, ATOM vs HETATM extraction, calculating resolution, domain classification.", table_cell)
        ],
        [
            Paragraph("<b>Mod 5: Function & Pathways</b>", table_cell_bold),
            Paragraph("Pfam (HMMs), PROSITE patterns/profiles, Gene Ontology (BP, MF, CC), EC classes, KEGG, BioGRID, STRING, DIP.", table_cell),
            Paragraph("Writing PROSITE regex, interpreting KEGG wiring diagrams, constructing PPI networks & confidence scores.", table_cell)
        ],
        [
            Paragraph("<b>Mod 6: Genome & Microarray</b>", table_cell_bold),
            Paragraph("Ensembl, UCSC Genome Browser (Tracks, BLAT), DNA Microarray (Cy3/Cy5), GEO (GSM, GSE, GPL, GDS), SAGE.", table_cell),
            Paragraph("UCSC BLAT genomic alignment, track visual navigation, GEO accession retrieval & probe mapping.", table_cell)
        ],
    ]
    t_syl = Table(syl_data, colWidths=[110, 230, 183])
    t_syl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_syl)
    story.append(Spacer(1, 14))

    # =============================================================
    # PART 1: COMPREHENSIVE THEORY & QUIZ PREPARATION
    # =============================================================
    story.append(make_banner("PART 1: COMPREHENSIVE THEORY & QUIZ PREPARATION", c_primary))
    story.append(Spacer(1, 8))

    # Module 1 Theory
    story.append(Paragraph("1. Module 1: Sequence Submission Tools & Molecular Data Formats", h1_style))
    story.append(Paragraph("<b>A. Motivation of Biological Databases & RDBMS:</b> Biological data generated by next-generation sequencing (NGS), mass spectrometry, and X-ray crystallography is massive, heterogeneous, and exponentially growing. Biological databases store, organize, index, and retrieve biological data systematically. A <b>Relational Database Management System (RDBMS)</b> organizes data into tables (relations) with predefined rows (tuples/records) and columns (attributes). Tables are interconnected through <i>Primary Keys</i> (unique identifiers within a table) and <i>Foreign Keys</i> (references to primary keys in another table). Relational algebra allows ACID compliance (Atomicity, Consistency, Isolation, Durability) and powerful SQL queries.", body_style))
    story.append(Paragraph("<b>B. Central Dogma of Molecular Biology:</b> Proposed by Francis Crick (1958). DNA undergoes semi-conservative <i>Replication</i>, is transcribed into mRNA by RNA Polymerase (<i>Transcription</i>), and mRNA codons (triplets) are translated into polypeptide chains on ribosomes by tRNA (<i>Translation</i>). Reverse transcription (RNA $\\rightarrow$ DNA) occurs in retroviruses via Reverse Transcriptase.", body_style))
    story.append(Paragraph("<b>C. International Nucleotide Sequence Collaboration (INSDC):</b> Composed of GenBank (NCBI, USA), ENA/EMBL-Bank (EMBL-EBI, Europe), and DDBJ (NIG, Japan). They exchange newly submitted nucleotide data on a daily synchronized basis. Once an accession number is granted by any of the three, it is globally recognized and universal.", body_style))
    story.append(Paragraph("<b>D. Sequence Submission Portals:</b>", h2_style))
    story.append(Paragraph("• <b>BankIt (NCBI):</b> Web-based questionnaire wizard. Designed for simple submissions: single/few mRNA, genomic DNA, organellar DNA, ribosomal RNA (16S/18S/ITS), or viral sequences. No local software installation needed.", bullet_style))
    story.append(Paragraph("• <b>Sequin (NCBI):</b> Standalone graphical program developed by NCBI for complex, long, or multi-segmented genomes. (Note: Officially retired by NCBI in favor of the web Submission Portal, but frequently tested in exams).", bullet_style))
    story.append(Paragraph("• <b>Webin (EMBL-EBI):</b> Standard submission system for nucleotide sequences, raw reads (SRA), assembled genomes, and transcriptomes to ENA.", bullet_style))
    story.append(Paragraph("• <b>SAKURA / D-way (DDBJ):</b> Web-based data submission system operated by the National Institute of Genetics (NIG) in Japan.", bullet_style))
    story.append(Paragraph("<b>E. Molecular Sequence Formats:</b>", h2_style))
    story.append(Paragraph("• <b>FASTA (.fasta / .fa):</b> Starts with '>' line followed by sequence ID and optional description. Subsequent lines contain pure 1-letter codes. Line breaks typically occur at 60 or 80 characters.", bullet_style))
    story.append(Paragraph("• <b>GenBank Flat File (.gb / .gbk):</b> Rich text record with labeled tokens: LOCUS (length, molecule, division, date), DEFINITION, ACCESSION, VERSION (includes GI number historically), DBASE, SOURCE, REFERENCE, FEATURES (CDS, gene, exon coordinates, /translation), ORIGIN (numbered base sequence ending in '//').", bullet_style))
    story.append(Paragraph("• <b>EMBL Format (.dat):</b> Uses two-character line codes: ID (identification), AC (accession), SV (sequence version), DE (description), KW (keywords), OS (organism species), OC (organism classification), FH/FT (feature header/table), SQ (sequence header), and terminates with '//'.", bullet_style))
    story.append(Paragraph("• <b>PIR / NBRF:</b> Starts with '>P1;' or '>F1;' followed by identifier, second line is description, sequence ends with an asterisk '*'.", bullet_style))
    story.append(Paragraph("• <b>Format Interconversion:</b> Carried out by web tools like <b>ReadSeq</b> (Don Gilbert) or command-line EMBOSS utility <b>seqret</b>.", bullet_style))

    story.append(Spacer(1, 6))

    # Module 3 Theory
    story.append(Paragraph("2. Module 3: Nucleotide and Protein Sequence Databases", h1_style))
    story.append(Paragraph("<b>A. Primary vs. Secondary Databases:</b> Primary databases contain raw archival experimental submissions without manual curation (GenBank, ENA, DDBJ, PDB). Secondary databases are derived, curated, non-redundant, and computationally or expert-annotated (RefSeq, Swiss-Prot, Pfam, PROSITE).", body_style))
    story.append(Paragraph("<b>B. UniProt Knowledgebase (UniProtKB):</b> The central hub for functional protein information. Formed by the UniProt Consortium (EMBL-EBI, SIB, and PIR). Consists of two sections:", body_style))
    story.append(Paragraph("• <b>UniProtKB/Swiss-Prot:</b> Manually annotated and reviewed by expert biocurators. Features high-quality functional descriptions, domain boundaries, post-translational modifications (PTMs), variants, and literature citations. Extremely low redundancy.", bullet_style))
    story.append(Paragraph("• <b>UniProtKB/TrEMBL:</b> (Translated EMBL). High-throughput, automatically translated and computationally annotated from open reading frames (CDS) of ENA/GenBank/DDBJ. Not yet reviewed by human curators.", bullet_style))
    story.append(Paragraph("• <b>PIR (Protein Information Resource):</b> Founded by Margaret Dayhoff (pioneer of bioinformatics who created the PAM matrix). Developed the Protein Sequence Database (PIR-PSD), now integrated into UniProt.", bullet_style))
    story.append(Paragraph("<b>C. Genetic Disorders & Mutation Databases:</b>", h2_style))
    story.append(Paragraph("• <b>COSMIC (Catalogue Of Somatic Mutations In Cancer):</b> Curated by the Wellcome Sanger Institute. World's most comprehensive resource for somatic mutation data in human cancers (point mutations, fusions, copy-number variants, drug resistance).", bullet_style))
    story.append(Paragraph("• <b>ClinVar (NCBI):</b> Public archive of relationships between human genomic variations and observed clinical phenotypes, with supporting evidence. Variants are categorized as: <i>Pathogenic</i>, <i>Likely Pathogenic</i>, <i>Uncertain Significance (VUS)</i>, <i>Likely Benign</i>, or <i>Benign</i>.", bullet_style))
    story.append(Paragraph("• <b>dbSNP (NCBI):</b> Repository for short genetic variations (single nucleotide variations, short deletions/insertions, microsatellites). Assigns a permanent reference SNP cluster ID: <b>rsID</b> (e.g., `rs1801133`). Submitter-level records have `ssIDs` before being clustered into an `rsID`.", bullet_style))

    story.append(Spacer(1, 6))

    # Module 4 Theory
    story.append(Paragraph("3. Module 4: Protein Structure Databases & Classification", h1_style))
    story.append(Paragraph("<b>A. Protein Data Bank (PDB):</b> Worldwide repository for 3D macromolecular structures of proteins and nucleic acids, managed by the **wwPDB** consortium (RCSB PDB, PDBe, PDBj, BMRB).", body_style))
    story.append(Paragraph("• <b>Experimental Methods:</b> X-ray Crystallography (~85% of PDB; measures electron density, reports atomic resolution in Ångströms; $\\le 2.0\\text{ Å}$ is considered high resolution); Nuclear Magnetic Resonance (NMR; captures ensemble of conformations in solution, reports distance constraints); Cryo-Electron Microscopy (Cryo-EM; high-resolution for large complexes without crystallization).", bullet_style))
    story.append(Paragraph("• <b>PDB Format Structure:</b> 80-column fixed-width text records. Key record types: `HEADER`, `COMPND`, `REMARK 2` (Resolution), `SEQRES` (Primary sequence), `ATOM` (Standard coordinates of protein/nucleic acid atoms), `HETATM` (Hetero-atoms: water, ions, ligands, inhibitors), `CONECT` (Bond connections), `TER` (End of chain).", bullet_style))
    story.append(Paragraph("• <b>mmCIF (macromolecular Crystallographic Information File):</b> Modern replacement for PDB flat files that eliminates limitations on chain count (>62 chains) and atom count (>99,999 atoms).", bullet_style))
    story.append(Paragraph("<b>B. Hierarchical Structural Classification Systems:</b>", h2_style))
    story.append(Paragraph("Proteins share structural folds even when sequence similarity is undetectable ($<20\\%$ identity). Two premier classification databases:", body_style))

    scop_cath_data = [
        [Paragraph("Feature", table_header), Paragraph("SCOP (Structural Classification of Proteins)", table_header), Paragraph("CATH (Class, Architecture, Topology, Homology)", table_header)],
        [
            Paragraph("<b>Founders & Origin</b>", table_cell_bold),
            Paragraph("Alexey Murzin et al. (MRC LMB, Cambridge, 1995).", table_cell),
            Paragraph("Christine Orengo et al. (UCL, London, 1997).", table_cell)
        ],
        [
            Paragraph("<b>Methodology</b>", table_cell_bold),
            Paragraph("<b>Largely manual / visual inspection</b> by experts.", table_cell),
            Paragraph("<b>Semi-automated</b>: algorithms (SSAP) + expert curation.", table_cell)
        ],
        [
            Paragraph("<b>Hierarchy Levels</b>", table_cell_bold),
            Paragraph("<b>1. Class:</b> Overall secondary structure composition.<br/><b>2. Fold:</b> Common structural core arrangements.<br/><b>3. Superfamily:</b> Probable common evolutionary origin.<br/><b>4. Family:</b> Clear evolutionary relationship ($>30\\%$ identity).", table_cell),
            Paragraph("<b>1. C (Class):</b> Secondary structure composition.<br/><b>2. A (Architecture):</b> Spatial orientation, no connectivity.<br/><b>3. T (Topology):</b> Fold & connectivity of secondary elements.<br/><b>4. H (Homologous Superfamily):</b> Common ancestry.", table_cell)
        ],
        [
            Paragraph("<b>Unique Level</b>", table_cell_bold),
            Paragraph("<b>Fold:</b> Groups proteins with similar secondary structure topologies regardless of evolutionary relationship.", table_cell),
            Paragraph("<b>Architecture:</b> Describes overall shape (e.g., $\\alpha-\\beta$ barrel, sandwich, roll) independent of loop connectivity.", table_cell)
        ]
    ]
    t_scop_cath = Table(scop_cath_data, colWidths=[90, 215, 218])
    t_scop_cath.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_scop_cath)

    story.append(Spacer(1, 6))

    # Module 5 Theory
    story.append(Paragraph("4. Module 5: Protein Function, Pathway and Interaction Databases", h1_style))
    story.append(Paragraph("<b>A. Pfam (Protein Families Database):</b> Comprehensive collection of protein domains and families represented by <b>Hidden Markov Models (Profile HMMs)</b> generated using the `HMMER` software package. Pfam consists of two tiers: <b>Pfam-A</b> (high-quality, manually curated seed alignments and curated thresholds) and <b>Pfam-B</b> (automated, uncurated clusters from ADDA).", body_style))
    story.append(Paragraph("<b>B. PROSITE (Signatures and Profiles):</b> Identifies functional sites, motifs, and domains using two methods:", body_style))
    story.append(Paragraph("• <b>Patterns:</b> Strict regular expressions representing conserved active sites. Rules: `[AC]` means Ala or Cys; `{ED}` means neither Glu nor Asp; `x` means any amino acid; `x(4)` means four arbitrary residues; `x(2,4)` means 2 to 4 residues; `<` means N-terminal; `>` means C-terminal. Example: `[LIVM]-x(2)-[LIVM]-x(2)-[LIVM]`.", bullet_style))
    story.append(Paragraph("• <b>Profiles:</b> Position-Specific Scoring Matrices (PSSMs) incorporating insertion and deletion penalties to model divergent domain families.", bullet_style))
    story.append(Paragraph("<b>C. Gene Ontology (GO):</b> Provides a standardized, controlled, species-independent vocabulary for gene and protein attributes. GO is structured as a <b>Directed Acyclic Graph (DAG)</b> where terms can have multiple parents. Three strictly defined organizing domains:", body_style))
    story.append(Paragraph("• <b>Molecular Function (MF):</b> Elemental biochemical activities (e.g., `catalytic activity`, `kinase activity`, `ATP binding`).", bullet_style))
    story.append(Paragraph("• <b>Biological Process (BP):</b> Broad biological objectives executed by multiple molecular steps (e.g., `signal transduction`, `cell division`, `glycolysis`).", bullet_style))
    story.append(Paragraph("• <b>Cellular Component (CC):</b> Subcellular anatomy or macromolecular complexes where the gene acts (e.g., `mitochondrial inner membrane`, `ribosome`, `nucleus`).", bullet_style))
    story.append(Paragraph("<b>D. ENZYME & Enzyme Commission (EC Numbers):</b> Classification scheme based on reaction type, consisting of 4 numbers: `EC a.b.c.d`.", body_style))
    story.append(Paragraph("• <b>EC 1: Oxidoreductases</b> (Oxidation-reduction reactions; dehydrogenases, oxidases).<br/>• <b>EC 2: Transferases</b> (Transfer of chemical groups: methyl, phosphate; kinases, methyltransferases).<br/>• <b>EC 3: Hydrolases</b> (Hydrolytic cleavage of bonds: esterases, nucleases, proteases).<br/>• <b>EC 4: Lyases</b> (Non-hydrolytic/non-oxidative cleavage forming double bonds; decarboxylases).<br/>• <b>EC 5: Isomerases</b> (Geometric or structural changes within a molecule; epimerases, mutases).<br/>• <b>EC 6: Ligases</b> (Joining two molecules coupled with ATP hydrolysis; synthetases, DNA ligase).<br/>• <b>EC 7: Translocases</b> (Movement of ions or molecules across membranes).", bullet_style))
    story.append(Paragraph("<b>E. KEGG (Kyoto Encyclopedia of Genes and Genomes):</b> Integrates genomic, chemical, and systemic functional information. Features <b>KEGG PATHWAY</b> (manually drawn wiring diagrams of metabolic and signaling networks). Each node represents a <b>KEGG Orthology (KO)</b> identifier (e.g., `K00844` for Hexokinase).", body_style))
    story.append(Paragraph("<b>F. Protein-Protein Interaction (PPI) Databases:</b>", h2_style))
    story.append(Paragraph("• <b>BioGRID:</b> Biomedical interaction repository curating physical interactions (Co-IP, Affinity Capture) and genetic interactions (synthetic lethality) directly from primary literature.", bullet_style))
    story.append(Paragraph("• <b>STRING (Search Tool for the Retrieval of Interacting Genes/Proteins):</b> Predicts physical and functional interactions. Integrates multi-evidence channels: <i>Gene Neighborhood, Gene Fusion, Co-occurrence, Co-expression, Experimental Assays, Curated Databases, and Automated Text Mining</i>. Assigns a combined confidence score ($0.0 - 1.0$; $\\ge 0.7$ is high confidence).", bullet_style))
    story.append(Paragraph("• <b>DIP (Database of Interacting Proteins):</b> Curates experimentally determined physical protein interactions, subjected to automated and manual quality checks (DIP Core set).", bullet_style))

    story.append(Spacer(1, 6))

    # Module 6 Theory
    story.append(Paragraph("5. Module 6: Genome and Microarray Databases", h1_style))
    story.append(Paragraph("<b>A. Genome Browsers:</b> Interactive graphical representations of annotated reference genomes.", body_style))
    story.append(Paragraph("• <b>Ensembl (EMBL-EBI / Sanger):</b> Automated gene annotation pipeline for chordate/vertebrate genomes. Integrates comparative genomics, gene trees, regulatory features, and <b>BioMart</b> for batch filtering and export.", bullet_style))
    story.append(Paragraph("• <b>UCSC Genome Browser:</b> Highly responsive genome visualizer developed at UC Santa Cruz. Displays annotations as horizontal 'Tracks' (Genes, ESTs, SNPs, Repeats, Conservation, ENCODE regulation). Features <b>BLAT</b> (Blast-Like Alignment Tool; ultra-fast mRNA/DNA mapping) and <b>Table Browser</b> for querying tabular genomic coordinates.", bullet_style))
    story.append(Paragraph("<b>B. DNA Microarray Principles & Technology:</b>", h2_style))
    story.append(Paragraph("Based on high-throughput microscopic nucleic acid hybridization between labeled target cDNA and known immobilized probe oligonucleotides on a solid substrate (glass chip).", body_style))
    story.append(Paragraph("• <b>Two-Color Microarray (cDNA):</b> Experimental sample labeled with Cy5 (Red, 650 nm) and Control sample labeled with Cy3 (Green, 550 nm). Competitive hybridization to the same array. Yellow = equal expression ($Cy5/Cy3 = 1$); Red = upregulated in target; Green = downregulated in target.", bullet_style))
    story.append(Paragraph("• <b>Single-Channel Microarray (Affymetrix GeneChip):</b> In situ synthesized oligonucleotide 25-mers. Each sample is hybridized to a separate chip and detected using biotinylated cRNA and streptavidin-phycoerythrin.", bullet_style))
    story.append(Paragraph("<b>C. NCBI GEO (Gene Expression Omnibus):</b> The premier international public repository for high-throughput functional genomics data (Microarray, RNA-seq, ChIP-seq).", body_style))
    story.append(Paragraph("• <b>GEO Accession Hierarchy (Extremely Important!):</b><br/>"
                           "1. <b>GSM (GEO Sample):</b> Describes conditions, extraction, and quantitative expression values of an individual biological sample.<br/>"
                           "2. <b>GSE (GEO Series):</b> Group of related samples defining a complete study/experiment.<br/>"
                           "3. <b>GPL (GEO Platform):</b> Technical description of the array/sequencer (probe sequences, reporter IDs, manufacturer).<br/>"
                           "4. <b>GDS (GEO Dataset):</b> Curated, normalized, biologically comparable collections of GSMs.", bullet_style))
    story.append(Paragraph("<b>D. SAGE (Serial Analysis of Gene Expression):</b> Developed by Victor Velculescu and Bert Vogelstein (1995). Tag-based quantitative transcriptomics technique. Principles:", body_style))
    story.append(Paragraph("• mRNA is captured using oligo(dT) beads $\\rightarrow$ synthesized to cDNA $\\rightarrow$ cleaved with an anchoring restriction enzyme (e.g., <i>NlaIII</i>) $\\rightarrow$ ligated to linkers containing a recognition site for a tagging enzyme (e.g., <i>BsmFI</i> or <i>MmeI</i>) $\\rightarrow$ cleaves short 10–14 bp (or 21 bp in LongSAGE) sequence tags from a fixed position $\\rightarrow$ tags are ligated into ditags $\\rightarrow$ concatenated into long molecules $\\rightarrow$ sequenced $\\rightarrow$ tags are matched to known mRNA sequences.", bullet_style))
    story.append(Paragraph("• <b>Advantage over Microarray:</b> SAGE is open-ended (does not require prior knowledge of transcripts/probes; can discover novel genes) and provides digital absolute abundance counts. <b>Disadvantage:</b> Labor-intensive, costly, short tags can map ambiguously.", bullet_style))

    story.append(Spacer(1, 10))

    # =============================================================
    # QUIZ PRACTICE QUESTIONS (HIGH YIELD)
    # =============================================================
    story.append(make_banner("HIGH-YIELD QUIZ & MCQ PRACTICE QUESTIONS (WITH ANSWERS)", colors.HexColor("#742A2A")))
    story.append(Spacer(1, 8))

    quiz_items = [
        ("Q1: Which consortium synchronizes data daily between GenBank, ENA, and DDBJ?",
         "INSDC (International Nucleotide Sequence Database Collaboration)."),
        ("Q2: In UniProtKB, what is the primary difference between Swiss-Prot and TrEMBL?",
         "Swiss-Prot is manually annotated and reviewed by biocurators; TrEMBL is computationally generated and unreviewed."),
        ("Q3: What does an 'rs' prefix indicate in human genetic variation?",
         "Reference SNP cluster identifier in NCBI dbSNP (e.g., rs6025 for Factor V Leiden)."),
        ("Q4: Name the 4 hierarchical classification levels of CATH in exact order.",
         "Class (C), Architecture (A), Topology (T), Homologous superfamily (H)."),
        ("Q5: In a PDB coordinate file, which record type holds solvent (water) and inhibitor molecules?",
         "HETATM (Hetero atom). Standard amino acid/nucleic acid residues use ATOM."),
        ("Q6: What mathematical model forms the foundation of Pfam domain profiles?",
         "Hidden Markov Models (Profile HMMs), implemented via HMMER."),
        ("Q7: In PROSITE syntax, what does the pattern '[LIVM]-x(2)-[DE]' mean?",
         "A hydrophobic residue (Leu, Ile, Val, or Met), followed by any 2 amino acids, followed by an acidic residue (Asp or Glu)."),
        ("Q8: What are the three non-overlapping organizing principles of Gene Ontology (GO)?",
         "Molecular Function (MF), Biological Process (BP), and Cellular Component (CC)."),
        ("Q9: What is the primary enzyme class for DNA Ligase in the EC system?",
         "EC 6 (Ligases - enzymes that join two molecules coupled with hydrolysis of a pyrophosphate bond)."),
        ("Q10: In STRING network graphs, what does a light-blue line connecting two nodes signify?",
         "Curated database evidence (interaction verified from pathways or interaction databases)."),
        ("Q11: What are the four main accession prefixes in NCBI GEO and what does each represent?",
         "GSM = Sample, GSE = Series (Study), GPL = Platform (Array design), GDS = Curated Dataset."),
        ("Q12: In a two-color cDNA microarray, if a spot fluoresces bright green (Cy3), what does it mean?",
         "The gene is downregulated in the experimental/target sample (higher expression in control labeled with Cy3)."),
        ("Q13: Which database specifically catalogs somatic mutations found exclusively in human cancer tissues?",
         "COSMIC (Catalogue Of Somatic Mutations In Cancer)."),
        ("Q14: What is the specialized fast alignment tool integrated into the UCSC Genome Browser?",
         "BLAT (Blast-Like Alignment Tool)."),
        ("Q15: Why is SAGE considered a 'digital' gene expression method compared to microarrays?",
         "SAGE counts absolute discrete frequency of sequenced tag occurrences, whereas microarray measures analog fluorescence intensity.")
    ]

    for q, ans in quiz_items:
        story.append(Paragraph(f"<b>{q}</b>", ParagraphStyle('QStyle', parent=body_style, fontName='Helvetica-Bold', textColor=c_primary)))
        story.append(Paragraph(f"<b>Answer:</b> {ans}", ParagraphStyle('AStyle', parent=body_style, textColor=colors.HexColor("#276749"), leftIndent=10)))
        story.append(Spacer(1, 3))

    story.append(PageBreak())

    # =============================================================
    # PART 2: LAB PRACTICAL PROTOCOLS & EXAM TIPS
    # =============================================================
    story.append(make_banner("PART 2: LAB PRACTICAL PROTOCOLS, WORKFLOWS & VIVA TIPS", colors.HexColor("#2C5282")))
    story.append(Spacer(1, 8))

    story.append(Paragraph("1. Practical Protocol: Molecular Sequence Formats & Conversions", h1_style))
    story.append(Paragraph("<b>Lab Task 1: Converting Sequence Formats using ReadSeq or EMBOSS seqret:</b><br/>"
                           "In the lab exam, you will frequently be given a GenBank flat file and asked to convert it to FASTA, or vice versa, and isolate specific CDS regions.", body_style))
    
    story.append(Paragraph("<b>Exact Command-Line Syntax (EMBOSS seqret):</b>", h2_style))
    story.append(make_code_box("# Convert GenBank flatfile to FASTA format:\nseqret -sequence input.gbk -outseq output.fasta -osformat fasta\n\n# Convert FASTA to EMBL format:\nseqret -sequence input.fasta -outseq output.embl -osformat embl\n\n# Extract only the coding sequence (CDS) translation:\n# Parse the /translation=\"...\" field directly from GenBank FEATURES table"))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Web-Based ReadSeq Execution Steps:</b><br/>"
                           "1. Open ReadSeq (e.g., EBI ReadSeq or Indiana Univ server).<br/>"
                           "2. Paste sequence into input text box or upload `.gbk` file.<br/>"
                           "3. Under 'Output Format', select 'FASTA / Pearson' or 'EMBL'.<br/>"
                           "4. Ensure 'Case' is preserved (Upper) and click 'Format' / 'Submit'.<br/>"
                           "5. Save the generated file with extension `.fasta`.", body_style))

    story.append(Spacer(1, 6))

    story.append(Paragraph("2. Practical Protocol: NCBI GenBank Submission via BankIt", h1_style))
    story.append(Paragraph("<b>Step-by-Step Practical Submission Workflow:</b><br/>"
                           "• <b>Step 1: Contact Information:</b> Enter submitter name, department, institution, country, and email.<br/>"
                           "• <b>Step 2: Reference Information:</b> Specify unpublished manuscript status, working title, and author list.<br/>"
                           "• <b>Step 3: Sequencing Technology:</b> Indicate Sanger sequencing or Next-Gen platform (Illumina, PacBio, Nanopore).<br/>"
                           "• <b>Step 4: Organism & Source Modifiers:</b> Enter scientific name (e.g., <i>Escherichia coli</i>), isolate/strain ID, tissue type, country of isolation.<br/>"
                           "• <b>Step 5: Sequence Upload:</b> Upload FASTA-formatted sequence file. Ensure FASTA header contains matching `[organism=...]` and `[isolate=...]` modifier tags.<br/>"
                           "• <b>Step 6: Feature Annotation:</b> Specify feature intervals (e.g., CDS `54..1420`, gene name, product name). Check for premature stop codons in translation.<br/>"
                           "• <b>Step 7: Review & Submit:</b> Validate warnings and submit to receive a temporary submission tracking number followed by the final Accession Number (e.g., `PQ123456`).", body_style))

    story.append(Spacer(1, 6))

    story.append(Paragraph("3. Practical Protocol: Protein Data Bank (PDB) Coordinate Parsing", h1_style))
    story.append(Paragraph("<b>Lab Task 2: Distinguishing & Extracting Coordinates (ATOM vs. HETATM):</b><br/>"
                           "Examiners often ask: <i>'Find the resolution of PDB 1TUP and write down the coordinates of the first bound zinc atom or ligand.'</i>", body_style))

    story.append(Paragraph("<b>Key PDB Line Anatomy:</b>", h2_style))
    story.append(make_code_box("REMARK   2 RESOLUTION.    1.80 ANGSTROMS.\nATOM      1  N   MET A   1      27.340  24.430   2.614  1.00  9.67           N\nATOM      2  CA  MET A   1      26.266  25.413   2.842  1.00 10.38           C\nHETATM 3294 ZN    ZN A 401      18.420  15.110  12.330  1.00 15.20          ZN\nHETATM 3295  O   HOH A 501      31.220  28.910   4.150  1.00 12.40           O"))
    story.append(Spacer(1, 4))
    story.append(Paragraph("• <b>Resolution Check:</b> Search for `REMARK 2` line near the top of the file.<br/>"
                           "• <b>Isolating Ligand / Drug / Ion:</b> Filter records beginning with `HETATM`. Notice residue name (e.g., `ZN`, `ATP`, `STI` for Gleevec).<br/>"
                           "• <b>Columns Breakdown:</b> Columns 31–38 = X coordinate; 39–46 = Y coordinate; 47–54 = Z coordinate; 55–60 = Occupancy ($1.00$); 61–66 = Temperature / B-factor ($15.20$).", body_style))

    story.append(Spacer(1, 6))

    story.append(Paragraph("4. Practical Protocol: SCOP & CATH Structural Classification Query", h1_style))
    story.append(Paragraph("<b>How to Look Up a Protein's Structural Domains:</b><br/>"
                           "1. Open CATH portal (`cathdb.info`) or SCOPe (`scop.berkeley.edu`).<br/>"
                           "2. Enter PDB ID (e.g., `1TIM` for Triosephosphate Isomerase).<br/>"
                           "3. In <b>CATH</b>, observe the 4-number classification string (e.g., `3.20.20.10`):<br/>"
                           "   - <b>3:</b> Class = Alpha-Beta.<br/>"
                           "   - <b>20:</b> Architecture = Alpha-Beta Barrel (TIM barrel).<br/>"
                           "   - <b>20:</b> Topology = TIM Barrel.<br/>"
                           "   - <b>10:</b> Homologous Superfamily = Triosephosphate Isomerase-like.<br/>"
                           "4. In <b>SCOP</b>, locate the classification hierarchy: <i>Class $\\rightarrow$ Fold $\\rightarrow$ Superfamily $\\rightarrow$ Family</i>.", body_style))

    story.append(Spacer(1, 6))

    story.append(Paragraph("5. Practical Protocol: Functional Motif Scanning using PROSITE", h1_style))
    story.append(Paragraph("<b>Lab Task 3: Scanning a Sequence for Motifs via ScanProsite:</b><br/>"
                           "1. Navigate to <i>ScanProsite</i> (`prosite.expasy.org/scanprosite`).<br/>"
                           "2. Paste protein sequence or enter UniProt accession (e.g., `P04637`).<br/>"
                           "3. Choose 'Scan for patterns and profiles'. Click 'Start Scan'.<br/>"
                           "4. <b>Interpreting Results:</b> Distinguish between high-specificity profiles (hit domains like `P53_TAD`, `P53_DNA_BIND`) and short, non-specific patterns (e.g., PKC phosphorylation sites, N-glycosylation sites).", body_style))

    story.append(Spacer(1, 6))

    story.append(Paragraph("6. Practical Protocol: STRING & BioGRID Network Construction", h1_style))
    story.append(Paragraph("<b>Lab Task 4: Building a PPI Network & Customizing Confidence Scores:</b><br/>"
                           "1. Open STRING (`string-db.org`). Select 'Protein by name'.<br/>"
                           "2. Enter gene symbol (e.g., `TP53`) and organism (`Homo sapiens`). Click Search.<br/>"
                           "3. <b>Interaction Network Display:</b> Each circle is a protein node; lines (edges) represent predicted/demonstrated interactions.<br/>"
                           "4. <b>Setting Confidence Threshold:</b> Go to 'Settings' $\\rightarrow$ Set 'Minimum required interaction score' to <b>Highest confidence (0.900)</b> or <b>Medium (0.400)</b>.<br/>"
                           "5. <b>Turning Evidence Channels On/Off:</b> Uncheck 'Textmining' to retain only experimentally verified or database-supported interactions.<br/>"
                           "6. <b>Functional Enrichment:</b> Click 'Analysis' tab to view enriched GO terms (Biological Process, Molecular Function) and KEGG pathways with FDR values.", body_style))

    story.append(Spacer(1, 6))

    story.append(Paragraph("7. Practical Protocol: UCSC Genome Browser & BLAT Search", h1_style))
    story.append(Paragraph("<b>Lab Task 5: Genomic Localization & BLAT Alignment:</b><br/>"
                           "1. Go to `genome.ucsc.edu` $\\rightarrow$ Tools $\\rightarrow$ <b>BLAT</b>.<br/>"
                           "2. Select Genome: 'Human', Assembly: 'Dec. 2013 (GRCh38/hg38)'.<br/>"
                           "3. Paste query nucleotide sequence or primer. Click 'Submit'.<br/>"
                           "4. In the BLAT Results table, select the top hit with $100\\%$ identity and click 'browser'.<br/>"
                           "5. <b>Navigating the Genome Browser Window:</b><br/>"
                           "   - Chromosome ideogram shows the cytoband (e.g., `17p13.1`).<br/>"
                           "   - Gene tracks: 'NCBI RefSeq' or 'GENCODE' show exons (solid blocks) and introns (lines with arrows denoting 5' to 3' strand direction).<br/>"
                           "   - Track configuration: Right click any track to change mode: <i>Hide, Dense, Squish, Pack, Full</i>. (Exam tip: 'Pack' or 'Full' shows individual transcript isoforms!).", body_style))

    story.append(Spacer(1, 6))

    story.append(Paragraph("8. Practical Protocol: Gene Expression Omnibus (GEO) Query", h1_style))
    story.append(Paragraph("<b>Lab Task 6: Retrieving Microarray Datasets and Exploring Samples:</b><br/>"
                           "1. Access NCBI GEO (`ncbi.nlm.nih.gov/geo`).<br/>"
                           "2. Enter a study accession in the search box: e.g., `GSE19804` (Non-smoking female lung cancer).<br/>"
                           "3. <b>Identifying Metadata Components:</b><br/>"
                           "   - <b>Platforms (GPL):</b> Identify chip used (e.g., `GPL570 [HG-U133_Plus_2] Affymetrix Human Genome U133 Plus 2.0 Array`).<br/>"
                           "   - <b>Samples (GSM):</b> Inspect sample count (e.g., 120 samples: 60 paired tumor vs normal tissues).<br/>"
                           "   - <b>Data Download:</b> 'Series Matrix File(s)' contains normalized log2 expression values ready for R/Python/Excel analysis; 'RAW' contains `.CEL` files.", body_style))

    story.append(Spacer(1, 10))

    # =============================================================
    # 25 TOP VIVA VOCE QUESTIONS WITH MODEL ANSWERS
    # =============================================================
    story.append(make_banner("TOP 25 VIVA VOCE QUESTIONS & EXAMINER TRAPS", colors.HexColor("#285E61")))
    story.append(Spacer(1, 8))

    viva_items = [
        ("1. What is the difference between an accession number and a version number?",
         "An Accession Number (e.g., NM_000546) is a permanent, immutable identifier for a record. The Version Number (e.g., NM_000546.6) increments whenever changes or updates are made to the underlying sequence."),
        ("2. How does RefSeq differ fundamentally from GenBank?",
         "GenBank is an archival, redundant database of direct author submissions that can contain duplicates and errors. RefSeq (NCBI) is non-redundant, expertly curated, and provides reference standard sequences (identified by an underscore in accession: NM_, NP_, NC_)."),
        ("3. What does '//' mean at the end of a GenBank or EMBL flat file?",
         "It signifies the termination / end-of-record marker for that biological entry."),
        ("4. What are the three letters following 'P1;' in a PIR format?",
         "P1 indicates a protein sequence in PIR/NBRF format. F1 indicates a nucleic acid sequence."),
        ("5. Why are somatic mutations cataloged in COSMIC not typically found in dbSNP?",
         "dbSNP catalogs germline variations and common polymorphisms across populations, whereas COSMIC exclusively catalogs acquired somatic mutations occurring specifically in tumor tissues."),
        ("6. What is the significance of the B-factor (temperature factor) in a PDB file?",
         "B-factor reflects the thermal mobility or static displacement/disorder of that atom in the crystal lattice. Higher B-factors indicate greater flexibility or uncertainty in atomic position."),
        ("7. What is the difference between SCOP and CATH in handling multi-domain proteins?",
         "Both databases split multi-domain proteins into individual structural domain units before classifying each domain independently."),
        ("8. In CATH, can two proteins with different topologies share the same Architecture?",
         "Yes! Architecture only considers the overall 3D shape and orientation of secondary structure elements, regardless of how loops connect them. Topology requires identical connectivity."),
        ("9. In a PROSITE pattern, what does '[ST]-x-[RK]' represent?",
         "Serine or Threonine, followed by any single residue, followed by Arginine or Lysine (a classic substrate recognition motif for certain kinases)."),
        ("10. What is an EC number for Hexokinase?",
         "EC 2.7.1.1 (Transferase -> Phosphotransferase -> with an alcohol group as acceptor)."),
        ("11. What is a Directed Acyclic Graph (DAG) in the context of Gene Ontology?",
         "A network where nodes (GO terms) are connected by directed edges (e.g., 'is_a', 'part_of') with no closed loops, allowing a specific child term to have multiple parent terms."),
        ("12. What are the five main edge colors in STRING networks and their meanings?",
         "Green: Neighborhood; Red: Fusion; Blue: Co-occurrence; Black: Co-expression; Pink: Experimental data; Light blue: Curated databases; Yellow: Text mining."),
        ("13. Why is BioGRID referred to as a curated literature repository?",
         "Because all recorded physical and genetic interactions in BioGRID are extracted and validated by expert biocurators reading primary peer-reviewed scientific literature."),
        ("14. What is the difference between a physical and a genetic interaction in BioGRID?",
         "A physical interaction means direct binding between proteins (detected via Yeast Two-Hybrid, Co-IP). A genetic interaction means the phenotype of a double mutant deviates from expectation (e.g., synthetic lethality), implying shared pathways without direct contact."),
        ("15. What is the primary advantage of BLAT over BLAST in the UCSC Genome Browser?",
         "BLAT indexes the entire genome into memory using non-overlapping k-mers, making it roughly 500 times faster for finding near-identical matches ($>95\\%$ similarity) across vertebrate genomes."),
        ("16. In UCSC, what is the difference between 'Dense' and 'Pack' track display modes?",
         "'Dense' collapses all features into a single solid black horizontal line. 'Pack' displays all transcript isoforms separately with arrows showing strand direction."),
        ("17. What is the role of an anchoring enzyme (e.g., NlaIII) in SAGE?",
         "It cleaves cDNA at a frequent 4-base recognition site (CATG) to ensure all tags are generated from a consistent, defined position near the 3' end of transcripts."),
        ("18. In two-color microarrays, what dye is traditionally used for Cy3 and Cy5?",
         "Cy3 fluoresces Green (~570 nm); Cy5 fluoresces Red (~670 nm)."),
        ("19. What is a 'probe set' in an Affymetrix GeneChip?",
         "A group of 11 to 20 probe pairs (25-mers) representing different regions of the same target mRNA transcript."),
        ("20. What is a GEO Series Matrix file?",
         "A pre-formatted, tab-delimited text file containing the normalized expression matrix of all samples (GSMs) in a study, accompanied by sample phenotype descriptions."),
        ("21. Can Swiss-Prot accession numbers change?",
         "Accession numbers in Swiss-Prot are stable and permanent. If entries merge, secondary accession numbers are retained to track provenance."),
        ("22. How do you identify the resolution of a crystal structure in a PDB file?",
         "Look at the `REMARK   2 RESOLUTION. <number> ANGSTROMS.` record near the top of the PDB header."),
        ("23. What does 'VUS' mean in ClinVar?",
         "Variant of Uncertain Significance - a detected variation where current evidence is insufficient to classify it as definitively pathogenic or benign."),
        ("24. What is the key functional role of KEGG Orthology (KO)?",
         "KO links genes across diverse species to an identical functional node in a reference pathway based on sequence homology."),
        ("25. Which software is used to build and query Pfam HMM profiles?",
         "The HMMER software suite (commands: `hmmbuild`, `hmmsearch`, `hmmscan`).")
    ]

    for q, a in viva_items:
        story.append(Paragraph(f"<b>{q}</b>", ParagraphStyle('VQ', parent=body_style, fontName='Helvetica-Bold', textColor=c_primary)))
        story.append(Paragraph(f"<b>Answer:</b> {a}", ParagraphStyle('VA', parent=body_style, textColor=colors.HexColor("#1A202C"), leftIndent=10)))
        story.append(Spacer(1, 2))

    story.append(Spacer(1, 10))
    story.append(make_callout("Review the ATOM vs HETATM columns and the CATH vs SCOP hierarchy levels right before stepping into the viva room. These are the two most frequently tested spotting questions!"))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {filename}")

if __name__ == "__main__":
    out_pdf = os.path.join(os.getcwd(), "BioDB_Complete_Preparation_Guide.pdf")
    build_pdf(out_pdf)
