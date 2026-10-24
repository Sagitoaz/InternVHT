"""Generate the three source-grounded UML diagrams. Standard library only."""
from pathlib import Path
import html
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
BLUE = '#e8f0fe'
GREEN = '#e7f3e8'
YELLOW = '#fff6d5'
INK = '#334155'

def label(value):
    return html.escape(value).replace('\n', '<br>')

class Diagram:
    def __init__(self, filename, title, width, height, subtitle):
        self.filename = filename
        self.width, self.height = width, height
        self.n = 1
        self.doc = ET.Element('mxfile', host='app.diagrams.net', type='device', version='24.7.17')
        page = ET.SubElement(self.doc, 'diagram', id=filename, name=title)
        self.model = ET.SubElement(page, 'mxGraphModel', grid='1', gridSize='10', page='1', pageScale='1', pageWidth=str(width), pageHeight=str(height), guides='1', connect='1', arrows='1', fold='1')
        self.root = ET.SubElement(self.model, 'root')
        ET.SubElement(self.root, 'mxCell', id='0')
        ET.SubElement(self.root, 'mxCell', id='1', parent='0')
        self.text(title, 35, 20, width-70, 45, size=26, bold=True)
        self.text(subtitle, 35, 70, width-70, 35, size=17)
    def vertex(self, value, x, y, w, h, style='', parent='1'):
        self.n += 1
        ident = 'c'+str(self.n)
        c = ET.SubElement(self.root, 'mxCell', id=ident, value=value, parent=parent, vertex='1', style=style or f'rounded=1;whiteSpace=wrap;html=1;fillColor={BLUE};strokeColor={INK};fontSize=16;spacing=10;')
        ET.SubElement(c, 'mxGeometry', x=str(x), y=str(y), width=str(w), height=str(h), attrib={'as':'geometry'})
        return ident
    def text(self, value, x, y, w, h, size=15, bold=False, parent='1', align='left'):
        return self.vertex(label(value),x,y,w,h,f'text;whiteSpace=wrap;html=1;strokeColor=none;fillColor=none;fontSize={size};fontStyle={int(bold)};align={align};verticalAlign=middle;spacing=4;',parent)
    def edge(self, a, b, text='', kind='flow', points=None, ports=''):
        self.n += 1
        kinds = {
            'flow':'endArrow=block;endFill=1;endSize=10;',
            'dependency':'dashed=1;endArrow=open;endFill=0;endSize=10;',
            'extends':'endArrow=block;endFill=0;endSize=18;',
            'implements':'dashed=1;endArrow=block;endFill=0;endSize=18;',
            'association':'endArrow=none;',
            'composition':'startArrow=diamond;startFill=1;startSize=16;endArrow=none;',
            'note':'dashed=1;endArrow=none;'
        }
        c=ET.SubElement(self.root,'mxCell',id='c'+str(self.n),parent='1',source=a,target=b,value=label(text),edge='1',style=f'edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor={INK};fontSize=14;labelBackgroundColor=#ffffff;'+kinds[kind]+ports)
        g=ET.SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'})
        if points:
            arr=ET.SubElement(g,'Array',attrib={'as':'points'})
            for x,y in points: ET.SubElement(arr,'mxPoint',x=str(x),y=str(y))
        return c
    def line(self, x1,y1,x2,y2,text='',dash=False,arrow='none',points=None,width=1):
        self.n+=1
        c=ET.SubElement(self.root,'mxCell',id='c'+str(self.n),parent='1',value=label(text),edge='1',style=f'html=1;strokeColor={INK};fontSize=14;labelBackgroundColor=#ffffff;strokeWidth={width};dashed={int(dash)};endArrow={arrow};endFill={int(arrow=="block")};')
        g=ET.SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'})
        ET.SubElement(g,'mxPoint',x=str(x1),y=str(y1),attrib={'as':'sourcePoint'})
        ET.SubElement(g,'mxPoint',x=str(x2),y=str(y2),attrib={'as':'targetPoint'})
        if points:
            arr=ET.SubElement(g,'Array',attrib={'as':'points'})
            for x,y in points: ET.SubElement(arr,'mxPoint',x=str(x),y=str(y))
    def note(self, text, x,y,w,h):
        return self.vertex(label(text),x,y,w,h,f'shape=note;whiteSpace=wrap;html=1;fillColor={YELLOW};strokeColor=#b59b49;fontSize=15;align=left;spacing=12;')
    def cls(self, name, fields, methods, x,y,w=380, stereo='', abstract=False):
        """Three separate compartments, each a child of the class rectangle."""
        header=55
        attr=max(38,23*len(fields)+15)
        ops=max(40,23*len(methods)+15)
        ident=self.vertex('',x,y,w,header+attr+ops,'rounded=0;html=1;fillColor=#ffffff;strokeColor='+INK+';container=1;collapsible=0;recursiveResize=0;')
        title=(f'«{stereo}»<br>' if stereo else '')+('<i>' if abstract else '')+'<b>'+html.escape(name)+'</b>'+('</i>' if abstract else '')
        self.vertex(title,0,0,w,header,'rounded=0;whiteSpace=wrap;html=1;fillColor='+ (GREEN if stereo in ('interface','record') else BLUE)+';strokeColor='+INK+';fontSize=16;align=center;',ident)
        self.vertex('<br>'.join(fields),0,header,w,attr,'rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor='+INK+';fontSize=14;align=left;verticalAlign=middle;spacing=10;',ident)
        self.vertex('<br>'.join(methods),0,header+attr,w,ops,'rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor='+INK+';fontSize=14;align=left;verticalAlign=middle;spacing=10;',ident)
        return ident
    def save(self):
        ET.indent(self.doc,space='  ')
        target=HERE/self.filename
        ET.ElementTree(self.doc).write(target,encoding='utf-8',xml_declaration=True)
        verify(target)
        return target

def safe(lines): return [html.escape(s) for s in lines]

def class_diagram():
    d=Diagram('class-diagram.drawio','Class diagram — Cấu trúc các lớp chính',2500,2490,'Ba ngăn: tên lớp / thuộc tính / phương thức. Tên và chữ ký lấy từ src/concurrent; lược bỏ constructor và getter thông thường.')
    c={}
    c['Main']=d.cls('Main',[],['<u>+ main(args: String[]): void</u>'],100,150,330)
    c['CliArgs']=d.cls('CliArgs',safe(['- processMode: ProcessMode','- threadCount: int','- file: String','- writeMode: WriteMode = NONE','- out: String = ""']),['<u>+ parse(args: String[]): CliArgs</u>'],100,420,330)
    c['ProcessMode']=d.cls('ProcessMode',safe(['BUFFERED, UNBUFFERED, QUEUE','EXECUTOR, VIRTUAL','- processName: String','- processorFactory: ProcessorFactory']),safe(['+ createProcess(threadCount: int,','  writer: RecordWriter): Processor']),100,840,330,'enumeration')
    c['WriteMode']=d.cls('WriteMode',safe(['NONE, UNSAFE','SYNCHRONIZE, REENTRANT_LOCK']),safe(['+ createWriter(out: String): RecordWriter']),100,1300,330,'enumeration')
    c['HashMapCounter']=d.cls('HashMapCounter',safe(['- counter: Map<String, Long>']),safe(['+ increase(word: String): void','+ getCount(): Map<String, Long>']),100,1730,330)
    c['Runner']=d.cls('Runner',safe(['- result: BenchmarkResult','- threadCount: int','- processName: String']),safe(['+ run(processor: Processor, file: String): void','+ getResult(): BenchmarkResult']),650,150,420)
    c['BenchmarkResult']=d.cls('BenchmarkResult',safe(['- seqProcessResult: ProcessResult','- processTime: long','- threadCount: int','- processName: String']),[],1170,150,420,'record')
    c['Processor']=d.cls('Processor',safe(['- wordCount: long','- lineCount: long','# result: ProcessResult']),['<i>+ process(file: String): void</i>']+safe(['+ getResult(): ProcessResult','# createResult(words: long, lines: long): void']),650,515,420,abstract=True)
    c['ProcessResult']=d.cls('ProcessResult',safe(['- lineCount: long','- wordCount: long']),[],1170,550,420,'record')
    variants=[('SeqBufProcessor',550,920,['- counter: HashMapCounter']),('SeqUnbufProcessor',950,920,['- counter: HashMapCounter']),('BlockingQueueProcessor',1350,920,['- workerCount: int','- writer: RecordWriter','- queue: BlockingQueue<FileRecord>']),('ExecutorQueueProcessor',550,1270,['- workerCount: int','- writer: RecordWriter','- queue: BlockingQueue<FileRecord>']),('VirtualThreadProcessor',950,1270,['- workerCount: int','- writer: RecordWriter'])]
    for name,x,y,attrs in variants:
        c[name]=d.cls(name,safe(attrs),safe(['+ process(file: String): void']),x,y,350)
    c['RecordProducer']=d.cls('RecordProducer',safe(['- queue: BlockingQueue<FileRecord>','- file: String']),safe(['+ run(): void']),550,1640,350)
    c['RecordConsumer']=d.cls('RecordConsumer',safe(['- queue: BlockingQueue<FileRecord>','- writer: RecordWriter','- wordCount: long','- processCount: long']),safe(['+ run(): void','- process(record: FileRecord): ProcessedRecord','+ getProcessCount(): long','+ getWordCount(): long']),1020,1640,490)
    c['FileRecord']=d.cls('FileRecord',safe(['- id: long','- originalText: String'])+['<u>+ POISION_PILL: FileRecord = (-1, "")</u>'],[],550,2080,350,'record')
    c['ProcessedRecord']=d.cls('ProcessedRecord',safe(['- id: long','- originalText: String','- modifiedText: String','- wordCount: int','- processedBy: String','- virtualThread: boolean']),[],1020,2070,490,'record')
    c['RecordWriter']=d.cls('RecordWriter',[],safe(['+ write(record: ProcessedRecord): void','+ close(): void']),1870,150,520,'interface')
    c['ResultWriter']=d.cls('ResultWriter',[],safe(['+ write(result: BenchmarkResult, message: String): void','+ write(result: BenchmarkResult): void {default}']),1870,630,520,'interface')
    c['BufferedResultWriter']=d.cls('BufferedResultWriter',safe(['- out: String']),safe(['+ write(result: BenchmarkResult, message: String): void']),1870,1030,520)
    d.edge(c['Main'],c['CliArgs'],'«use» parse','dependency')
    d.edge(c['Main'],c['Runner'],'«create» / run','dependency')
    d.edge(c['CliArgs'],c['ProcessMode'],'processMode 1','association')
    d.edge(c['CliArgs'],c['WriteMode'],'writeMode 1','association',[(60,560),(60,1370)],'exitX=0;exitY=0.5;entryX=0;entryY=0.5;')
    d.edge(c['Runner'],c['Processor'],'«use» process','dependency')
    d.edge(c['Runner'],c['BenchmarkResult'],'result 0..1','association')
    d.edge(c['BenchmarkResult'],c['ProcessResult'],'seqProcessResult 0..1','association')
    d.edge(c['Processor'],c['ProcessResult'],'result 0..1','association')
    for name,x,y,attrs in variants:
        pts=[(x+175,860),(860,860)]
        if name=='ExecutorQueueProcessor': pts=[(725,1220),(510,1220),(510,860),(860,860)]
        if name=='VirtualThreadProcessor': pts=[(1125,1220),(1320,1220),(1320,860),(860,860)]
        d.edge(c[name],c['Processor'],'','extends',pts,'exitX=0.5;exitY=0;entryX=0.5;entryY=1;')
    d.edge(c['SeqBufProcessor'],c['HashMapCounter'],'counter 1','composition',[(465,995),(465,1800)],'exitX=0;exitY=0.5;entryX=1;entryY=0.4;')
    d.edge(c['SeqUnbufProcessor'],c['HashMapCounter'],'counter 1','composition',[(1125,1190),(485,1190),(485,1860)],'exitX=0.5;exitY=1;entryX=1;entryY=0.8;')
    d.edge(c['RecordProducer'],c['FileRecord'],'«create»','dependency')
    d.edge(c['RecordConsumer'],c['ProcessedRecord'],'«create»','dependency')
    d.edge(c['RecordConsumer'],c['RecordWriter'],'writer 1','association',[(1830,1800),(1830,310)],'exitX=1;exitY=0.5;entryX=0;entryY=1;')
    d.edge(c['BufferedResultWriter'],c['ResultWriter'],'','implements')
    writers=d.note('RecordWriter được triển khai bởi:\n• NoOpsRecordWriter — không ghi\n• UnsafeRecordWriter — không khóa toàn record\n• SynchronizedRecordWriter — synchronized\n• LockRecordWriter — ReentrantLock\nCác lớp này được lược khỏi hình để tránh dày sơ đồ.',1870,400,520,180)
    d.edge(writers,c['RecordWriter'],'','note')
    d.note('Pipeline ở 3 mode đồng thời:\nTạo 1 RecordProducer và N RecordConsumer.\nHai bên giữ cùng queue ArrayBlockingQueue(1000).\nProducer và consumer implements Runnable (JDK).\nBUFFERED/UNBUFFERED chỉ đếm; không dùng writer.\nLược bỏ dependency tạo worker để đường nối rõ hơn.',1870,1350,520,175)
    d.note('Ký hiệu UML\n+ public; - private; # protected\nGạch chân: static; chữ nghiêng: abstract\nTam giác rỗng nét liền: generalization (extends)\nTam giác rỗng nét đứt: realization (implements)\nNét liền: association; số ở nhãn là multiplicity\nThoi đặc phía chủ sở hữu: composition\nNét đứt mũi tên mở: dependency\n«record»: trường private final; accessor sinh tự động.',1870,1640,520,280)
    d.note('Phạm vi: cấu trúc chính, không liệt kê mọi getter/constructor. Các lớp phụ ProcessorFactory, WordCounter, WriteHelper và writer khác giữ nguyên trong source.\nLargeFileGenerator sinh dữ liệu thử; lời gọi Main.genFile() hiện bị comment.\nLỗi source: cả 3 processor đồng thời gọi createResult(totalRecords, totalWords) — đảo ý nghĩa tham số, dẫn đến báo cáo đảo số dòng/từ.',80,2380,2310,90)
    # Emphasize the retained structural relationships without changing the
    # styling of the sequence and activity diagrams.
    for cell in d.root:
        if cell.get('edge')=='1':
            style=cell.get('style','')
            is_note='dashed=1;endArrow=none;' in style
            width=2 if is_note else 3
            cell.set('style',style+f'strokeWidth={width};strokeColor=#0f172a;')
            if 'endArrow=block;endFill=0;' in style:
                cell.set('style',cell.get('style')+'endSize=22;')
            if 'startArrow=diamond;' in style:
                cell.set('style',cell.get('style')+'startSize=20;')
    return d

class Sequence(Diagram):
    def frame(self,kind,guard,x,y,w,h):
        self.vertex('',x,y,w,h,'rounded=0;fillColor=none;strokeColor=#64748b;html=1;')
        self.vertex(label(kind),x,y,65,30,'shape=umlFrame;fillColor=#f1f5f9;strokeColor=#64748b;html=1;align=center;fontStyle=1;fontSize=14;')
        offset=145 if kind=='ref' else 80
        self.text(guard,x+offset,y+2,w-offset-15,26,size=14)
    def head(self,key,role,title,x,y=150):
        self.x[key]=x
        if role=='actor':
            self.vertex('',x-22,y,44,65,'shape=umlActor;fillColor=#ffffff;strokeColor='+INK+';')
        elif role in ('boundary','control','entity'):
            self.vertex('',x-24,y+5,48,48,'ellipse;fillColor=#ffffff;strokeColor='+INK+';')
            if role=='boundary':
                self.line(x-43,y+5,x-43,y+53); self.line(x-43,y+29,x-24,y+29)
            if role=='entity': self.line(x-28,y+57,x+28,y+57)
            if role=='control': self.line(x-7,y+5,x+17,y+5,arrow='open')
        else:
            self.vertex('',x-50,y,100,55,'rounded=0;fillColor=#ffffff;strokeColor='+INK+';')
        self.text(('«'+role+'»\n' if role!='actor' else '')+title,x-105,y+65,210,68,align='center',size=14)
        self.line(x,y+138,x,self.height-160,dash=True)
    def activation(self,key,y,h):
        self.vertex('',self.x[key]-7,y,14,h,'rounded=0;fillColor=#ffffff;strokeColor='+INK+';')
    def message(self,a,b,y,text,reply=False,async_=False):
        x1=self.x[a]; x2=self.x[b]
        if a==b:
            self.line(x1+7,y,x1+7,y+40,text,reply,'open' if reply else 'block',[(x1+75,y),(x1+75,y+40)])
        else:
            self.line(x1,y,x2,y,text,reply,'open' if reply or async_ else 'block')

def sequence_diagram():
    d=Sequence('sequence-diagram.drawio','Sequence diagram — Luồng chạy cơ bản',1880,2070,'Đọc cấu hình → xử lý file → lấy kết quả → ghi báo cáo. Có actor, boundary/control/entity, activation và đường trả về.')
    d.x={}
    for key,role,title,x in [
        ('user','actor','Người chạy CLI',120),
        ('main','control','main : Main',310),
        ('cli','boundary','cli : CliArgs',530),
        ('runner','control','runner : Runner',750),
        ('proc','control','processor : Processor',990),
        ('writer','boundary','writer : RecordWriter',1240),
        ('report','boundary','resWriter : BufferedResultWriter',1510)
    ]:
        d.head(key,role,title,x)
    # Each fragment has its own empty header band, at least 55 px above calls.
    d.frame('ref','Tạo writer / processor theo WriteMode và ProcessMode',220,520,1110,65)
    d.frame('opt','[chế độ đồng thời]',925,985,520,295)
    d.head('result','entity','result : BenchmarkResult',1730,y=1470)
    for key,y,h in [('main',340,1520),('cli',410,60),('runner',650,910),
                    ('proc',730,590),('proc',1380,60),('writer',1040,60),
                    ('writer',1160,60),('runner',1620,60),('report',1740,60)]:
        d.activation(key,y,h)
    d.message('user','main',340,'main(args)')
    d.message('main','cli',410,'parse(args)')
    d.message('cli','main',470,'config : CliArgs',reply=True)
    d.message('main','runner',650,'run(processor, file)')
    d.message('runner','proc',730,'process(file) — bắt đầu đo')
    d.note('TUẦN TỰ: đọc file, đếm dòng và từ.\nĐỒNG THỜI: producer → queue → N consumer;\nđếm từ, chuyển chữ hoa, ghi nếu bật.',825,805,720,135)
    d.message('proc','writer',1040,'write(record)')
    d.message('writer','proc',1100,'void',reply=True)
    d.text('Chờ worker xong, tổng hợp bộ đếm',1010,1125,420,25,size=13)
    d.message('proc','writer',1160,'close()')
    d.message('writer','proc',1220,'void',reply=True)
    d.message('proc','runner',1320,'void — xử lý xong',reply=True)
    d.message('runner','proc',1380,'getResult() — kết thúc đo')
    d.message('proc','runner',1440,'ProcessResult',reply=True)
    d.line(d.x['runner'],1500,d.x['result']-26,1500,'«create» new BenchmarkResult(...)',arrow='open')
    d.message('runner','main',1560,'void',reply=True)
    d.message('main','runner',1620,'getResult()')
    d.message('runner','main',1680,'BenchmarkResult',reply=True)
    d.message('main','report',1740,'write(result) → results.txt')
    d.message('report','main',1800,'void',reply=True)
    d.message('main','user',1860,'Kết thúc; hiển thị kết quả',reply=True)
    d.note('Processor đại diện toàn bộ xử lý bên trong; write(record) là lời gọi từ consumer, lặp cho các bản ghi.\nKhung opt chỉ áp dụng QUEUE / EXECUTOR / VIRTUAL; hai chế độ tuần tự không dùng RecordWriter.\nRunner.run() và Processor.process() trả void; kết quả được lấy bằng getResult() riêng.',35,1940,1810,110)
    return d

class Activity(Diagram):
    def action(self,text,x,y,w=390,h=85): return self.vertex(label(text),x,y,w,h)
    def diamond(self,text,x,y,w=185,h=105): return self.vertex(label(text),x,y,w,h,'rhombus;whiteSpace=wrap;html=1;fillColor='+YELLOW+';strokeColor='+INK+';fontSize=15;spacing=5;')
    def bar(self,x,y,w): return self.vertex('',x,y,w,10,'rounded=0;fillColor='+INK+';strokeColor='+INK+';')
    def final(self,x,y):
        outer=self.vertex('',x,y,36,36,'ellipse;fillColor=#ffffff;strokeColor='+INK+';strokeWidth=2;')
        self.vertex('',8,8,20,20,'ellipse;fillColor='+INK+';strokeColor='+INK+';',outer)
        return outer

def activity_diagram():
    d=Activity('activity-diagram.drawio','Activity diagram — Luồng xử lý cơ bản',1530,1640,'Hai nhánh xử lý: tuần tự hoặc đồng thời; cùng trả kết quả để đo thời gian và ghi báo cáo.')
    for title,x,w in [('Main / Runner',30,430),('Processor',480,600),('Ghi báo cáo',1100,400)]:
        d.vertex(label(title),x,130,w,1470,'swimlane;startSize=45;html=1;fillColor=#f1f5f9;swimlaneFillColor=#ffffff;strokeColor=#cbd5e1;fontSize=18;fontStyle=1;')
    start=d.vertex('',230,190,30,30,'ellipse;fillColor='+INK+';strokeColor='+INK+';')
    config=d.action('Đọc cấu hình CLI\nMode, N, file vào/ra và cách ghi',70,270,350,80); d.edge(start,config)
    setup=d.action('Tạo writer, processor và Runner',70,405,350,80); d.edge(config,setup)
    timer=d.action('Bắt đầu đo thời gian\nGọi processor.process(file)',70,550,350,80); d.edge(setup,timer)
    mode=d.diamond('Chế độ xử lý?',665,535,220,110); d.edge(timer,mode)
    seq=d.action('BUFFERED / UNBUFFERED\nĐọc file tuần tự\nĐếm dòng và từ',505,735,260,125); d.edge(mode,seq,'[tuần tự]')
    concurrent=d.action('QUEUE / EXECUTOR / VIRTUAL\nProducer → queue → N consumer\nĐếm từ, chuyển chữ hoa\nGhi từng record nếu bật',795,725,260,155); d.edge(mode,concurrent,'[đồng thời]')
    wait=d.action('Chờ worker hoàn tất\nTổng hợp số đếm\nĐóng RecordWriter',795,950,260,105); d.edge(concurrent,wait)
    merge=d.diamond('',750,1120,60,60); d.edge(seq,merge); d.edge(wait,merge)
    result=d.action('Kết thúc đo thời gian\nTạo BenchmarkResult',70,1220,350,85); d.edge(merge,result,points=[(780,1195),(245,1195)])
    report=d.action('Append báo cáo vào results.txt\nFlush và đóng file',1140,1220,330,85); d.edge(result,report)
    output=d.action('In kết quả ra console',70,1400,350,70); d.edge(report,output,points=[(1305,1360),(245,1360)])
    end=d.final(227,1530); d.edge(output,end)
    d.note('Producer và consumer chạy song song; chi tiết queue, vòng lặp và poison pill được gộp vào nhánh đồng thời.\nMã hiện tại đảo số dòng/từ ở ba mode đồng thời; sơ đồ mô tả luồng thành công.',490,1485,1010,90)
    for cell in d.root:
        if cell.get('edge')=='1':
            cell.set('style',cell.get('style')+'strokeWidth=2.5;strokeColor=#0f172a;')
    return d

def verify(path):
    root=ET.parse(path).getroot()
    assert root.tag=='mxfile' and len(root)==1, path
    model=root[0].find('mxGraphModel')
    cells=model.find('root')
    by_id={c.get('id'):c for c in cells}
    assert len(by_id)==len(cells)
    for cell in cells:
        for k in ('parent','source','target'):
            if cell.get(k): assert cell.get(k) in by_id, (path,cell.get('id'),k)
        if cell.get('vertex')=='1':
            geo=cell.find('mxGeometry')
            x,y,w,h=[float(geo.get(k,'0')) for k in ('x','y','width','height')]
            parent=cell.get('parent')
            if parent!='1':
                pg=by_id[parent].find('mxGeometry')
                assert x>=0 and y>=0 and x+w<=float(pg.get('width'))+.1 and y+h<=float(pg.get('height'))+.1
            else:
                assert x>=0 and y>=0 and x+w<=float(model.get('pageWidth')) and y+h<=float(model.get('pageHeight')), (path,cell.get('value'))
    print(path.name, 'XML / endpoints / compartments / bounds: OK')

def semantic_checks():
    cls=ET.parse(HERE/'class-diagram.drawio').getroot()
    cells=cls.findall('.//mxCell')
    assert len([c for c in cells if 'endArrow=block;endFill=0;' in c.get('style','') and 'dashed=1' not in c.get('style','')])==5
    assert len([c for c in cells if 'dashed=1;endArrow=block;endFill=0;' in c.get('style','')])==1
    for c in cells:
        if 'container=1' in c.get('style',''):
            assert len([n for n in cells if n.get('parent')==c.get('id')])==3
    seq=ET.parse(HERE/'sequence-diagram.drawio').getroot()
    edges=[c for c in seq.findall('.//mxCell') if c.get('edge')=='1']
    assert len([c for c in edges if c.get('value') and 'dashed=1' in c.get('style','')])==9
    assert len([c for c in seq.findall('.//mxCell') if c.get('value')==label('opt')])==1
    labels=' '.join(c.get('value','') for c in seq.findall('.//mxCell'))
    assert all(role in labels for role in ['boundary','control','entity'])
    activity=ET.parse(HERE/'activity-diagram.drawio').getroot()
    ac=activity.findall('.//mxCell')
    assert len([c for c in ac if 'swimlane;' in c.get('style','')])==3
    assert not [c for c in ac if c.get('value')=='lặp']
    for cell in ac:
        if cell.get('vertex')=='1' and 'rounded=1;' in cell.get('style',''):
            incoming=[edge for edge in ac if edge.get('target')==cell.get('id')]
            assert len(incoming)==1, ('action with implicit join',cell.get('value'))
    for cell in ac:
        if cell.get('vertex')=='1' and 'rhombus;' in cell.get('style',''):
            incoming=[edge for edge in ac if edge.get('target')==cell.get('id')]
            outgoing=[edge for edge in ac if edge.get('source')==cell.get('id')]
            if cell.get('value'):
                assert len(incoming)==1 and len(outgoing)==2, ('decision',cell.get('value'))
                assert all(edge.get('value') for edge in outgoing)
            else:
                assert len(incoming)>=2 and len(outgoing)==1, ('merge',cell.get('id'))
    print('Semantic checks: class relations preserved; sequence has 9 replies and one opt; activity has 3 lanes, guarded branches and a merge: OK')

if __name__=='__main__':
    diagrams=[class_diagram(),sequence_diagram(),activity_diagram()]
    for diagram in diagrams: diagram.save()
    semantic_checks()
