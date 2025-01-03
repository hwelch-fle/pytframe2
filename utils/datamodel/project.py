from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Generator

import arcpy.mp as mp
import arcpy._mp as mptype

@dataclass
class Layer:
    layer: mptype.Layer

@dataclass
class Table:
    table: mptype.Table

@dataclass
class Map:
    _map: mptype.Map

    def __post_init__(self):
        self.name: str = self._map.name
        self.layers: list[Layer] = [Layer(l) for l in self._map.listLayers()]
        self.tables: list[Table] = [Table(t) for t in self._map.listTables()]

@dataclass
class PDFSettings:
    out_pdf: Path=None
    page_range_type:Literal[
        'ALL', 
        'CURRENT', 
        'RANGE', 
        'SELECTED']="CURRENT"
    page_range_string: str=""
    multiple_files: Literal[
        'PDF_SINGLE_FILE', 
        'PDF_MULTIPLE_FILES_PAGE_NAME', 
        'PDF_MULTIPLE_FILES_PAGE_NUMBER']="PDF_SINGLE_FILE"
    resolution: int=96
    image_quality: Literal[
        'BEST', 
        'BETTER', 
        'FASTER', 
        'FASTEST', 
        'NORMAL']='BEST'
    compress_vector_graphics: bool=True
    image_compression: Literal[
        'ADAPTIVE',
        'DEFLATE',
        'JPEG',
        'JPEG2000',
        'LZW',
        'NONE',
        'RLE']='ADAPTIVE'
    embed_fonts: bool=True
    layers_attributes: Literal[
        'LAYERS_AND_ATTRIBUTES',
        'LAYERS_ONLY',
        'NONE']='LAYERS_ONLY'
    georef_info: bool=True
    jpeg_compression_quality: int=80
    clip_to_elements: bool=False
    show_selection_symbology: bool=False
    output_as_image: bool=False
    embed_color_profile: bool=True
    pdf_accessibility: bool=False
    show_export_count: bool=False
    keep_layout_background: bool=True
    convert_markers: bool=False
    simulate_overprint: bool=False

@dataclass
class MapSeries:
    _mapseries: mptype.MapSeries
    _export_settings: PDFSettings=None
    
    def __len__(self):
        return self._mapseries.pageCount

    def __getitem__(self, index: int):
        self._mapseries.currentPageNumber = index
        return
    
    def refresh(self):
        self._mapseries.refresh()
    
    @property
    def current_page(self):
        return self._mapseries.currentPageNumber
    
    @current_page.setter
    def current_page(self, value: int):
        self._mapseries.currentPageNumber = value
    
    def page_row(self) -> dict:
        return self._mapseries.pageRow._asdict()
    
    def current_page_name(self):
        return self.page_row()[self._mapseries.pageNameField.name]
    
    @property
    def export_settings(self):
        return self._export_settings
    
    @export_settings.setter
    def export_settings(self, value: PDFSettings):
        self._export_settings = value
        
    def exportCurrentToPDF(self, out_path: Path=None, settings: PDFSettings=None) -> Path:
        if not settings:
            settings = self._export_settings
        if out_path:
            settings.out_pdf = out_path
        self._mapseries.exportToPDF(**settings.__dict__)
        return settings.out_pdf
    
    def exportAllToPDF(self, out_path: Path, settings: PDFSettings=None) -> Generator[Path, None, None]:
        if not settings:
            settings = self._export_settings
        for page in range(1, len(self)+1):
            self.current_page = page
            settings.out_pdf = str(Path(out_path) / f"_{self.current_page_name()}.pdf")
            self._mapseries.exportToPDF(**settings.__dict__)
            yield settings.out_pdf

@dataclass
class Layout:
    _layout: mptype.Layout
    _export_settings: PDFSettings=None
    
    def __post_init__(self):
        self.name: str = self._layout.name
        self.mapseries: MapSeries = self._layout.mapSeries
        if self.mapseries:
            self.mapseries = MapSeries(self.mapseries, self._export_settings)
    
    @property
    def export_settings(self):
        return self._export_settings
    
    @export_settings.setter
    def export_settings(self, value: PDFSettings):
        self._export_settings = value

@dataclass
class Project:
    path: Path
    
    def __post_init__(self):
        self.project: mp.ArcGISProject = mp.ArcGISProject(self.path)
        self.maps: list[Map] = [Map(m) for m in self.project.listMaps()]
        self.layouts: list[Layout] = [Layout(l) for l in self.project.listLayouts()]
    
    def save(self):
        self.project.save()
    
    def save_copy(self, path: Path):
        self.project.saveACopy(path)