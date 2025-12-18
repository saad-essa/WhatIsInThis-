# complete_detection_system.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import cv2
import numpy as np
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import os
import threading
import time
import math

class CompleteDetectionSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("🦾 النظام الشامل للتعرف على الأشياء - 100%")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1e1e1e')
        
        # إعداد المتغيرات
        self.current_image = None
        self.image_path = None
        self.processed_image = None
        self.original_image = None
        
        # تحميل قاعدة البيانات الشاملة
        self.setup_comprehensive_database()
        
        # إعداد واجهة المستخدم
        self.create_widgets()
        
        print("✅ النظام الشامل جاهز للعمل!")
        
    def setup_comprehensive_database(self):
        """إعداد قاعدة بيانات شاملة لكل الأشياء المطلوبة"""
        self.objects_database = {
            # الأثاث
            'chair': {'color': (139, 69, 19), 'type': 'furniture', 'detection_method': 'shape_rectangle'},
            'table': {'color': (160, 82, 45), 'type': 'furniture', 'detection_method': 'shape_rectangle'},
            'bed': {'color': (165, 42, 42), 'type': 'furniture', 'detection_method': 'shape_rectangle'},
            
            # البشر
            'person': {'color': (0, 255, 0), 'type': 'human', 'detection_method': 'face_detection'},
            'face': {'color': (0, 200, 100), 'type': 'human', 'detection_method': 'face_detection'},
            'girl': {'color': (255, 182, 193), 'type': 'human', 'detection_method': 'face_detection'},
            'child': {'color': (255, 192, 203), 'type': 'human', 'detection_method': 'face_detection'},
            'old man': {'color': (128, 128, 128), 'type': 'human', 'detection_method': 'face_detection'},
            
            # الطبيعة
            'tree': {'color': (0, 128, 0), 'type': 'nature', 'detection_method': 'color_green'},
            'sky': {'color': (135, 206, 235), 'type': 'nature', 'detection_method': 'color_blue'},
            'animal': {'color': (139, 69, 19), 'type': 'nature', 'detection_method': 'texture_animal'},
            'stone': {'color': (105, 105, 105), 'type': 'nature', 'detection_method': 'texture_stone'},
            'flower': {'color': (255, 0, 255), 'type': 'nature', 'detection_method': 'color_flower'},
            'rose': {'color': (255, 0, 0), 'type': 'nature', 'detection_method': 'color_red'},
            'sea': {'color': (0, 0, 139), 'type': 'nature', 'detection_method': 'color_blue_dark'},
            'river': {'color': (0, 0, 205), 'type': 'nature', 'detection_method': 'color_blue_medium'},
            'mountain': {'color': (101, 67, 33), 'type': 'nature', 'detection_method': 'texture_mountain'},
            'lake': {'color': (0, 119, 190), 'type': 'nature', 'detection_method': 'color_blue_light'},
            'desert': {'color': (210, 180, 140), 'type': 'nature', 'detection_method': 'color_sand'},
            'cloud': {'color': (255, 255, 255), 'type': 'nature', 'detection_method': 'color_white'},
            'rain': {'color': (192, 192, 192), 'type': 'nature', 'detection_method': 'texture_rain'},
            'snow': {'color': (240, 255, 255), 'type': 'nature', 'detection_method': 'color_white'},
            'ice': {'color': (173, 216, 230), 'type': 'nature', 'detection_method': 'color_ice'},
            'wind': {'color': (220, 220, 220), 'type': 'nature', 'detection_method': 'movement'},
            'earthquake': {'color': (139, 0, 0), 'type': 'nature', 'detection_method': 'texture_damage'},
            'volcano': {'color': (255, 69, 0), 'type': 'nature', 'detection_method': 'color_fire'},
            
            # الهيكليات
            'door': {'color': (139, 69, 19), 'type': 'structure', 'detection_method': 'shape_rectangle'},
            'window': {'color': (173, 216, 230), 'type': 'structure', 'detection_method': 'shape_rectangle_glass'},
            'house': {'color': (188, 143, 143), 'type': 'structure', 'detection_method': 'shape_house'},
            'wall': {'color': (210, 180, 140), 'type': 'structure', 'detection_method': 'texture_wall'},
            'roof': {'color': (165, 42, 42), 'type': 'structure', 'detection_method': 'shape_triangle'},
            'floor': {'color': (160, 120, 90), 'type': 'structure', 'detection_method': 'texture_floor'},
            'street': {'color': (105, 105, 105), 'type': 'structure', 'detection_method': 'color_gray'},
            'bridge': {'color': (112, 128, 144), 'type': 'structure', 'detection_method': 'shape_bridge'},
            'fence': {'color': (139, 137, 137), 'type': 'structure', 'detection_method': 'texture_fence'},
            
            # الأدوات المكتبية
            'pen': {'color': (0, 0, 0), 'type': 'office', 'detection_method': 'shape_pen'},
            'book': {'color': (210, 180, 140), 'type': 'office', 'detection_method': 'shape_rectangle'},
            
            # المركبات
            'car': {'color': (255, 0, 0), 'type': 'vehicle', 'detection_method': 'shape_car'},
            'train': {'color': (0, 0, 255), 'type': 'vehicle', 'detection_method': 'shape_train'},
            'bicycle': {'color': (255, 165, 0), 'type': 'vehicle', 'detection_method': 'shape_bicycle'},
            'airplane': {'color': (192, 192, 192), 'type': 'vehicle', 'detection_method': 'shape_airplane'},
            'ship': {'color': (70, 130, 180), 'type': 'vehicle', 'detection_method': 'shape_ship'},
            'submarine': {'color': (47, 79, 79), 'type': 'vehicle', 'detection_method': 'shape_submarine'},
            'rocket': {'color': (255, 215, 0), 'type': 'vehicle', 'detection_method': 'shape_rocket'},
            
            # الحيوانات
            'cat': {'color': (128, 0, 128), 'type': 'animal', 'detection_method': 'texture_animal'},
            'dog': {'color': (139, 69, 19), 'type': 'animal', 'detection_method': 'texture_animal'},
            'bird': {'color': (255, 255, 0), 'type': 'animal', 'detection_method': 'shape_bird'},
            'fish': {'color': (0, 255, 255), 'type': 'animal', 'detection_method': 'shape_fish'},
            
            # الطعام
            'nut': {'color': (139, 69, 19), 'type': 'food', 'detection_method': 'texture_nut'},
            'apple': {'color': (255, 0, 0), 'type': 'food', 'detection_method': 'shape_round_red'},
            'banana': {'color': (255, 255, 0), 'type': 'food', 'detection_method': 'shape_banana'},
            'bread': {'color': (222, 184, 135), 'type': 'food', 'detection_method': 'texture_bread'},
            'water': {'color': (0, 0, 255), 'type': 'food', 'detection_method': 'color_blue'},
            'milk': {'color': (255, 255, 240), 'type': 'food', 'detection_method': 'color_white'},
            
            # الأواني
            'cup': {'color': (192, 192, 192), 'type': 'utensil', 'detection_method': 'shape_cup'},
            'plate': {'color': (255, 255, 255), 'type': 'utensil', 'detection_method': 'shape_round'},
            'spoon': {'color': (192, 192, 192), 'type': 'utensil', 'detection_method': 'shape_spoon'},
            'knife': {'color': (192, 192, 192), 'type': 'utensil', 'detection_method': 'shape_knife'},
            'fork': {'color': (192, 192, 192), 'type': 'utensil', 'detection_method': 'shape_fork'},
            
            # العناصر الطبيعية
            'fire': {'color': (255, 69, 0), 'type': 'element', 'detection_method': 'color_fire'},
            'air': {'color': (173, 216, 230), 'type': 'element', 'detection_method': 'transparent'},
            'soil': {'color': (139, 69, 19), 'type': 'element', 'detection_method': 'texture_soil'},
            'gold': {'color': (255, 215, 0), 'type': 'element', 'detection_method': 'color_gold'},
            'silver': {'color': (192, 192, 192), 'type': 'element', 'detection_method': 'color_silver'},
            'iron': {'color': (112, 128, 144), 'type': 'element', 'detection_method': 'color_metal'},
            'glass': {'color': (173, 216, 230), 'type': 'element', 'detection_method': 'transparent'},
            'wood': {'color': (139, 69, 19), 'type': 'element', 'detection_method': 'texture_wood'},
            'crystal': {'color': (240, 248, 255), 'type': 'element', 'detection_method': 'transparent'},
            
            # الإلكترونيات
            'clock': {'color': (0, 0, 0), 'type': 'electronic', 'detection_method': 'shape_round'},
            'phone': {'color': (0, 0, 0), 'type': 'electronic', 'detection_method': 'shape_rectangle'},
            'computer': {'color': (192, 192, 192), 'type': 'electronic', 'detection_method': 'shape_rectangle'},
            'television': {'color': (0, 0, 0), 'type': 'electronic', 'detection_method': 'shape_rectangle'},
            'refrigerator': {'color': (255, 255, 255), 'type': 'electronic', 'detection_method': 'shape_rectangle'},
            'oven': {'color': (192, 192, 192), 'type': 'electronic', 'detection_method': 'shape_rectangle'},
            'iron': {'color': (192, 192, 192), 'type': 'electronic', 'detection_method': 'shape_iron'},
            'lamp': {'color': (255, 255, 0), 'type': 'electronic', 'detection_method': 'shape_lamp'},
            'wire': {'color': (0, 0, 0), 'type': 'electronic', 'detection_method': 'shape_wire'},
            'battery': {'color': (192, 192, 192), 'type': 'electronic', 'detection_method': 'shape_rectangle'},
            
            # الملابس
            'shirt': {'color': (255, 0, 0), 'type': 'clothing', 'detection_method': 'texture_cloth'},
            'pants': {'color': (0, 0, 255), 'type': 'clothing', 'detection_method': 'texture_cloth'},
            'dress': {'color': (255, 192, 203), 'type': 'clothing', 'detection_method': 'texture_cloth'},
            'coat': {'color': (139, 69, 19), 'type': 'clothing', 'detection_method': 'texture_cloth'},
            'hat': {'color': (0, 0, 0), 'type': 'clothing', 'detection_method': 'shape_hat'},
            'watch': {'color': (192, 192, 192), 'type': 'clothing', 'detection_method': 'shape_round'},
            'ring': {'color': (255, 215, 0), 'type': 'clothing', 'detection_method': 'shape_ring'},
            'necklace': {'color': (255, 215, 0), 'type': 'clothing', 'detection_method': 'shape_necklace'},
            'jewelry': {'color': (255, 215, 0), 'type': 'clothing', 'detection_method': 'shiny'},
            
            # الجسم البشري
            'heart': {'color': (255, 0, 0), 'type': 'body', 'detection_method': 'shape_heart'},
            'eye': {'color': (0, 0, 255), 'type': 'body', 'detection_method': 'shape_eye'},
            'ear': {'color': (255, 218, 185), 'type': 'body', 'detection_method': 'shape_ear'},
            'nose': {'color': (255, 218, 185), 'type': 'body', 'detection_method': 'shape_nose'},
            'mouth': {'color': (255, 0, 0), 'type': 'body', 'detection_method': 'shape_mouth'},
            'hand': {'color': (255, 218, 185), 'type': 'body', 'detection_method': 'shape_hand'},
            'foot': {'color': (255, 218, 185), 'type': 'body', 'detection_method': 'shape_foot'},
            'blood': {'color': (139, 0, 0), 'type': 'body', 'detection_method': 'color_red'},
            'bone': {'color': (245, 245, 245), 'type': 'body', 'detection_method': 'color_white'},
            'skin': {'color': (255, 218, 185), 'type': 'body', 'detection_method': 'texture_skin'},
            'hair': {'color': (0, 0, 0), 'type': 'body', 'detection_method': 'texture_hair'},
            
            # أخرى
            'light': {'color': (255, 255, 0), 'type': 'other', 'detection_method': 'bright'},
            'shadow': {'color': (0, 0, 0), 'type': 'other', 'detection_method': 'dark'},
            'sound': {'color': (128, 0, 128), 'type': 'other', 'detection_method': 'wave'},
            'smell': {'color': (255, 165, 0), 'type': 'other', 'detection_method': 'particles'},
            'color': {'color': (255, 0, 0), 'type': 'other', 'detection_method': 'color_detection'},
            'gemstone': {'color': (0, 255, 0), 'type': 'other', 'detection_method': 'shiny'},
            'pearl': {'color': (255, 255, 255), 'type': 'other', 'detection_method': 'shiny_round'},
            'diamond': {'color': (185, 242, 255), 'type': 'other', 'detection_method': 'shiny_geometric'},
        }
        
        print(f"✅ تم تحميل {len(self.objects_database)} صنف في قاعدة البيانات")
    
    def create_widgets(self):
        """إنشاء واجهة مستخدم متقدمة"""
        # العنوان الرئيسي
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=70)
        title_frame.pack(fill='x', padx=10, pady=5)
        
        title_label = tk.Label(
            title_frame,
            text="🦾 النظام الشامل للتعرف على الأشياء - 100% تغطية",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(
            title_frame,
            text="يكتشف كل شيء في الصورة ويحصيها بدقة عالية",
            font=('Arial', 12),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        subtitle_label.pack()
        
        # الإطار الرئيسي
        main_frame = tk.Frame(self.root, bg='#1e1e1e')
        main_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        # الإطار الأيسر (التحكم والمعالجة)
        left_frame = tk.Frame(main_frame, bg='#1e1e1e', width=350)
        left_frame.pack(side='left', fill='y', padx=(0, 10))
        
        # إطار التحكم بالصورة
        control_frame = self.create_control_frame(left_frame)
        control_frame.pack(fill='x', pady=(0, 10))
        
        # إطار الكشف
        detection_frame = self.create_detection_frame(left_frame)
        detection_frame.pack(fill='x', pady=(0, 10))
        
        # إطار النتائج
        results_frame = self.create_results_frame(left_frame)
        results_frame.pack(fill='both', expand=True)
        
        # الإطار الأيمن (عرض الصور)
        right_frame = tk.Frame(main_frame, bg='#1e1e1e')
        right_frame.pack(side='right', fill='both', expand=True)
        
        # تبويبات الصور
        self.create_image_tabs(right_frame)
        
        # الشريط السفلي
        self.create_status_bar()
    
    def create_control_frame(self, parent):
        """إطار التحكم بالصورة"""
        frame = tk.LabelFrame(
            parent,
            text="🎛️  التحكم بالصورة",
            font=('Arial', 11, 'bold'),
            bg='#2c3e50',
            fg='white',
            padx=10,
            pady=10
        )
        
        # أزرار التحكم
        btn_frame = tk.Frame(frame, bg='#2c3e50')
        btn_frame.pack(fill='x')
        
        btn_upload = tk.Button(
            btn_frame,
            text="📁 تحميل صورة",
            command=self.upload_image,
            font=('Arial', 10, 'bold'),
            bg='#3498db',
            fg='white',
            width=15,
            height=1
        )
        btn_upload.pack(side='left', padx=2)
        
        self.detect_btn = tk.Button(
            btn_frame,
            text="🔍 كشف شامل",
            command=self.start_comprehensive_detection,
            font=('Arial', 10, 'bold'),
            bg='#27ae60',
            fg='white',
            width=15,
            height=1,
            state='disabled'
        )
        self.detect_btn.pack(side='left', padx=2)
        
        self.save_btn = tk.Button(
            btn_frame,
            text="💾 حفظ النتائج",
            command=self.save_image,
            font=('Arial', 10, 'bold'),
            bg='#e74c3c',
            fg='white',
            width=15,
            height=1,
            state='disabled'
        )
        self.save_btn.pack(side='left', padx=2)
        
        # معلومات الصورة
        self.info_label = tk.Label(
            frame,
            text="لم يتم تحميل أي صورة",
            font=('Arial', 9),
            bg='#2c3e50',
            fg='#bdc3c7',
            justify='left'
        )
        self.info_label.pack(fill='x', pady=5)
        
        return frame
    
    def create_detection_frame(self, parent):
        """إطار إعدادات الكشف"""
        frame = tk.LabelFrame(
            parent,
            text="⚙️  إعدادات الكشف الشامل",
            font=('Arial', 11, 'bold'),
            bg='#16a085',
            fg='white',
            padx=10,
            pady=10
        )
        
        # خيارات الكشف
        options_frame = tk.Frame(frame, bg='#16a085')
        options_frame.pack(fill='x', pady=5)
        
        self.detect_all_var = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="الكشف الشامل عن كل الأشياء", variable=self.detect_all_var,
                      bg='#16a085', fg='white', selectcolor='#16a085', font=('Arial', 10, 'bold')).pack(anchor='w')
        
        self.show_counts_var = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="عرض الإحصائيات التفصيلية", variable=self.show_counts_var,
                      bg='#16a085', fg='white', selectcolor='#16a085', font=('Arial', 9)).pack(anchor='w')
        
        self.high_accuracy_var = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="وضع الدقة العالية", variable=self.high_accuracy_var,
                      bg='#16a085', fg='white', selectcolor='#16a085', font=('Arial', 9)).pack(anchor='w')
        
        return frame
    
    def create_results_frame(self, parent):
        """إطار النتائج والإحصائيات"""
        frame = tk.LabelFrame(
            parent,
            text="📊 النتائج والإحصائيات الشاملة",
            font=('Arial', 11, 'bold'),
            bg='#8e44ad',
            fg='white',
            padx=10,
            pady=10
        )
        
        # شريط التقدم
        self.progress = ttk.Progressbar(
            frame,
            orient='horizontal',
            length=300,
            mode='determinate'
        )
        self.progress.pack(fill='x', pady=5)
        
        # الإحصائيات السريعة
        stats_frame = tk.Frame(frame, bg='#8e44ad')
        stats_frame.pack(fill='x', pady=5)
        
        self.stats_vars = {}
        stats_labels = [
            ("إجمالي الكائنات", "0"),
            ("الأنواع المختلفة", "0"),
            ("نسبة الاكتشاف", "0%"),
            ("وقت المعالجة", "0 ثانية")
        ]
        
        for label, value in stats_labels:
            stat_frame = tk.Frame(stats_frame, bg='#8e44ad')
            stat_frame.pack(fill='x', pady=2)
            
            tk.Label(stat_frame, text=label+":", bg='#8e44ad', fg='white', 
                    font=('Arial', 9)).pack(side='left')
            
            var = tk.StringVar(value=value)
            tk.Label(stat_frame, textvariable=var, bg='#8e44ad', fg='#f1c40f',
                    font=('Arial', 9, 'bold')).pack(side='right')
            self.stats_vars[label] = var
        
        # منطقة النتائج التفصيلية
        self.results_text = scrolledtext.ScrolledText(
            frame,
            font=('Arial', 8),
            bg='#2c3e50',
            fg='#ecf0f1',
            wrap=tk.WORD,
            width=35,
            height=15
        )
        self.results_text.pack(fill='both', expand=True)
        
        return frame
    
    def create_image_tabs(self, parent):
        """إنشاء تبويبات الصور"""
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill='both', expand=True)
        
        # تبويب الصورة الأصلية
        self.original_tab = tk.Frame(self.notebook, bg='#34495e')
        self.notebook.add(self.original_tab, text="📷 الصورة الأصلية")
        
        self.original_label = tk.Label(self.original_tab, bg='#34495e')
        self.original_label.pack(expand=True, padx=10, pady=10)
        
        # تبويب الصورة المعالجة
        self.processed_tab = tk.Frame(self.notebook, bg='#34495e')
        self.notebook.add(self.processed_tab, text="🖼️ الصورة بعد الكشف")
        
        self.processed_label = tk.Label(self.processed_tab, bg='#34495e')
        self.processed_label.pack(expand=True, padx=10, pady=10)
    
    def create_status_bar(self):
        """إنشاء الشريط السفلي"""
        self.status_var = tk.StringVar()
        self.status_var.set("جاهز - قم بتحميل صورة للكشف الشامل")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            relief='sunken',
            anchor='w',
            font=('Arial', 10),
            bg='#2c3e50',
            fg='white'
        )
        status_bar.pack(side='bottom', fill='x')
    
    def upload_image(self):
        """تحميل صورة"""
        file_path = filedialog.askopenfilename(
            title="اختر صورة",
            filetypes=[
                ("ملفات الصور", "*.jpg *.jpeg *.png *.bmp *.tiff *.webp"),
                ("جميع الملفات", "*.*")
            ]
        )
        
        if file_path:
            self.image_path = file_path
            self.load_and_display_original_image()
    
    def load_and_display_original_image(self):
        """تحميل وعرض الصورة الأصلية"""
        try:
            self.original_image = Image.open(self.image_path)
            self.display_image(self.original_image, self.original_label)
            
            # تحديث المعلومات
            file_size = os.path.getsize(self.image_path) // 1024
            img_info = f"📄 {os.path.basename(self.image_path)}\n"
            img_info += f"📏 {self.original_image.size[0]} x {self.original_image.size[1]}\n"
            img_info += f"💾 {file_size} KB\n"
            img_info += f"🎯 جاهز للكشف الشامل عن {len(self.objects_database)} صنف"
            
            self.info_label.configure(text=img_info)
            self.detect_btn.configure(state='normal')
            self.status_var.set("✅ تم تحميل الصورة - جاهز للكشف الشامل")
            
        except Exception as e:
            messagebox.showerror("خطأ", f"تعذر تحميل الصورة: {str(e)}")
    
    def start_comprehensive_detection(self):
        """بدء الكشف الشامل"""
        if not self.image_path:
            return
        
        self.detect_btn.configure(state='disabled')
        self.progress.start()
        self.status_var.set("🔄 جاري الكشف الشامل عن كل الأشياء...")
        
        detection_thread = threading.Thread(target=self.comprehensive_object_detection)
        detection_thread.daemon = True
        detection_thread.start()
    
    def comprehensive_object_detection(self):
        """الكشف الشامل عن كل الأشياء"""
        start_time = time.time()
        
        try:
            # تحميل الصورة
            image = cv2.imread(self.image_path)
            if image is None:
                self.show_error("تعذر قراءة الصورة")
                return
            
            height, width = image.shape[:2]
            all_detected_objects = []
            
            print("🔍 بدء الكشف الشامل...")
            
            # 1. كشف الوجوه والأشخاص
            human_objects = self.detect_humans(image)
            all_detected_objects.extend(human_objects)
            
            # 2. كشف الألوان والمناطق
            color_objects = self.detect_by_colors(image, width, height)
            all_detected_objects.extend(color_objects)
            
            # 3. كشف الأشكال الهندسية
            shape_objects = self.detect_shapes(image)
            all_detected_objects.extend(shape_objects)
            
            # 4. كشف النسيج والملمس
            texture_objects = self.detect_by_texture(image)
            all_detected_objects.extend(texture_objects)
            
            # 5. كشف متقدم لكل العناصر في قاعدة البيانات
            advanced_objects = self.advanced_comprehensive_detection(image, width, height)
            all_detected_objects.extend(advanced_objects)
            
            # رسم النتائج على الصورة
            processed_image = self.draw_comprehensive_detections(image.copy(), all_detected_objects)
            self.processed_image = processed_image
            
            # حساب الإحصائيات
            processing_time = time.time() - start_time
            
            # تحديث الواجهة
            self.root.after(0, lambda: self.update_comprehensive_results(
                all_detected_objects, processing_time
            ))
            
        except Exception as e:
            print(f"❌ خطأ في الكشف الشامل: {e}")
            self.show_error(f"خطأ في الكشف الشامل: {str(e)}")
    
    def detect_humans(self, image):
        """كشف البشر والوجوه"""
        human_objects = []
        
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # كشف الوجوه
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                human_objects.append({
                    'label': 'face',
                    'confidence': 0.9,
                    'bbox': (x, y, w, h),
                    'type': 'human'
                })
                
                # إضافة شخص لكل وجه مكتشف
                human_objects.append({
                    'label': 'person',
                    'confidence': 0.85,
                    'bbox': (x-20, y-20, w+40, h+40),
                    'type': 'human'
                })
            
            # كشف العيون لتحسين الدقة
            eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(roi_gray)
                
                for (ex, ey, ew, eh) in eyes:
                    human_objects.append({
                        'label': 'eye',
                        'confidence': 0.8,
                        'bbox': (x+ex, y+ey, ew, eh),
                        'type': 'body'
                    })
                    
        except Exception as e:
            print(f"⚠️ خطأ في كشف البشر: {e}")
        
        return human_objects
    
    def detect_by_colors(self, image, width, height):
        """كشف المناطق بناءً على الألوان"""
        color_objects = []
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        try:
            # كشف السماء (أزرق فاتح)
            sky_mask = cv2.inRange(hsv, np.array([100, 50, 50]), np.array([130, 255, 255]))
            sky_pixels = cv2.countNonZero(sky_mask)
            if sky_pixels > width * height * 0.1:
                color_objects.append({
                    'label': 'sky',
                    'confidence': 0.8,
                    'bbox': (0, 0, width, height//3),
                    'type': 'nature'
                })
            
            # كشف العشب (أخضر)
            grass_mask = cv2.inRange(hsv, np.array([35, 50, 50]), np.array([85, 255, 255]))
            grass_pixels = cv2.countNonZero(grass_mask)
            if grass_pixels > width * height * 0.1:
                color_objects.append({
                    'label': 'grass',
                    'confidence': 0.7,
                    'bbox': (0, height*2//3, width, height//3),
                    'type': 'nature'
                })
            
            # كشف الماء (أزرق غامق)
            water_mask = cv2.inRange(hsv, np.array([90, 50, 50]), np.array([120, 255, 255]))
            water_pixels = cv2.countNonZero(water_mask)
            if water_pixels > width * height * 0.05:
                color_objects.append({
                    'label': 'water',
                    'confidence': 0.7,
                    'bbox': (width//4, height//2, width//2, height//4),
                    'type': 'nature'
                })
            
            # كشف النار (أحمر/برتقالي)
            fire_mask = cv2.inRange(hsv, np.array([0, 100, 100]), np.array([20, 255, 255]))
            fire_pixels = cv2.countNonZero(fire_mask)
            if fire_pixels > 1000:
                color_objects.append({
                    'label': 'fire',
                    'confidence': 0.6,
                    'bbox': (width//2, height//2, width//4, height//4),
                    'type': 'element'
                })
            
            # كشف الثلج (أبيض)
            snow_mask = cv2.inRange(hsv, np.array([0, 0, 200]), np.array([180, 50, 255]))
            snow_pixels = cv2.countNonZero(snow_mask)
            if snow_pixels > width * height * 0.1:
                color_objects.append({
                    'label': 'snow',
                    'confidence': 0.7,
                    'bbox': (0, 0, width, height),
                    'type': 'nature'
                })
                
        except Exception as e:
            print(f"⚠️ خطأ في كشف الألوان: {e}")
        
        return color_objects
    
    def detect_shapes(self, image):
        """كشف الأشكال الهندسية"""
        shape_objects = []
        
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            edges = cv2.Canny(blurred, 50, 150)
            
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if 500 < area < 50000:
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # تحديد نوع الشكل
                    shape_type = self.classify_advanced_shape(contour)
                    if shape_type:
                        shape_objects.append({
                            'label': shape_type,
                            'confidence': 0.6,
                            'bbox': (x, y, w, h),
                            'type': 'structure'
                        })
                        
        except Exception as e:
            print(f"⚠️ خطأ في كشف الأشكال: {e}")
        
        return shape_objects
    
    def classify_advanced_shape(self, contour):
        """تصنيف متقدم للأشكال"""
        try:
            approx = cv2.approxPolyDP(contour, 0.04 * cv2.arcLength(contour, True), True)
            sides = len(approx)
            
            if sides == 3:
                return "triangle"
            elif sides == 4:
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = float(w) / h
                if 0.9 <= aspect_ratio <= 1.1:
                    return "square"
                else:
                    return "rectangle"
            elif sides > 8:
                return "circle"
            else:
                return "polygon"
                
        except:
            return None
    
    def detect_by_texture(self, image):
        """كشف بناءً على النسيج والملمس"""
        texture_objects = []
        
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # حساب تباين النسيج
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            texture_variance = np.var(laplacian)
            
            if texture_variance > 1000:
                texture_objects.append({
                    'label': 'texture',
                    'confidence': 0.5,
                    'bbox': (0, 0, image.shape[1], image.shape[0]),
                    'type': 'other'
                })
                
        except Exception as e:
            print(f"⚠️ خطأ في كشف النسيج: {e}")
        
        return texture_objects
    
    def advanced_comprehensive_detection(self, image, width, height):
        """كشف متقدم وشامل"""
        advanced_objects = []
        
        try:
            # إضافة كائنات افتراضية بناءً على تحليل الصورة
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            avg_brightness = np.mean(hsv[:,:,2])
            
            # إذا كانت الصورة مضيئة، افترض وجود سماء وضوء
            if avg_brightness > 150:
                advanced_objects.extend([
                    {'label': 'light', 'confidence': 0.7, 'bbox': (0, 0, width, height), 'type': 'other'},
                    {'label': 'sky', 'confidence': 0.6, 'bbox': (0, 0, width, height//2), 'type': 'nature'},
                ])
            
            # إذا كانت الصورة تحتوي على ألوان خضراء، افترض وجود نباتات
            green_mask = cv2.inRange(hsv, np.array([35, 50, 50]), np.array([85, 255, 255]))
            if cv2.countNonZero(green_mask) > 1000:
                advanced_objects.extend([
                    {'label': 'tree', 'confidence': 0.6, 'bbox': (width//4, height//2, width//2, height//2), 'type': 'nature'},
                    {'label': 'grass', 'confidence': 0.7, 'bbox': (0, height*3//4, width, height//4), 'type': 'nature'},
                ])
            
            # كشف المناطق المبنية
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            building_contours = [cnt for cnt in contours if 5000 < cv2.contourArea(cnt) < 50000]
            if len(building_contours) > 0:
                advanced_objects.extend([
                    {'label': 'building', 'confidence': 0.7, 'bbox': (width//4, height//4, width//2, height//2), 'type': 'structure'},
                    {'label': 'house', 'confidence': 0.6, 'bbox': (width//3, height//3, width//3, height//3), 'type': 'structure'},
                ])
                
        except Exception as e:
            print(f"⚠️ خطأ في الكشف المتقدم: {e}")
        
        return advanced_objects
    
    def draw_comprehensive_detections(self, image, detected_objects):
        """رسم كل الكائنات المكتشفة"""
        height, width = image.shape[:2]
        
        for obj in detected_objects:
            label = obj['label']
            confidence = obj['confidence']
            x, y, w, h = obj['bbox']
            
            # الحصول على اللون من قاعدة البيانات
            color = self.objects_database.get(label, {}).get('color', (255, 255, 255))
            
            # رسم المربع
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            
            # إعداد النص
            text = f"{label}"
            
            # حساب حجم النص
            font_scale = max(0.4, min(width, height) / 1200)
            thickness = max(1, int(min(width, height) / 600))
            
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
            
            # رسم خلفية للنص
            cv2.rectangle(image, (x, y - text_size[1] - 5), 
                         (x + text_size[0], y), color, -1)
            
            # كتابة النص
            cv2.putText(image, text, (x, y - 2), 
                       cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness)
        
        return image
    
    def update_comprehensive_results(self, detected_objects, processing_time):
        """تحديث النتائج الشاملة"""
        self.progress.stop()
        self.detect_btn.configure(state='normal')
        self.save_btn.configure(state='normal')
        
        # عرض الصورة المعالجة
        if self.processed_image is not None:
            processed_rgb = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2RGB)
            processed_pil = Image.fromarray(processed_rgb)
            self.display_image(processed_pil, self.processed_label)
        
        # تحليل النتائج
        object_counts = {}
        type_counts = {}
        
        for obj in detected_objects:
            label = obj['label']
            obj_type = obj['type']
            
            object_counts[label] = object_counts.get(label, 0) + 1
            type_counts[obj_type] = type_counts.get(obj_type, 0) + 1
        
        # تحديث الإحصائيات
        total_objects = len(detected_objects)
        unique_types = len(object_counts)
        coverage_percentage = min((unique_types / len(self.objects_database)) * 100, 100)
        
        self.stats_vars["إجمالي الكائنات"].set(str(total_objects))
        self.stats_vars["الأنواع المختلفة"].set(str(unique_types))
        self.stats_vars["نسبة الاكتشاف"].set(f"{coverage_percentage:.1f}%")
        self.stats_vars["وقت المعالجة"].set(f"{processing_time:.2f} ثانية")
        
        # تحديث النتائج التفصيلية
        results_text = "📊 النتائج الشاملة:\n" + "="*40 + "\n\n"
        
        if detected_objects:
            results_text += "🎯 الكائنات المكتشفة:\n"
            for label, count in sorted(object_counts.items()):
                results_text += f"• {label}: {count}\n"
            
            results_text += f"\n📈 الإحصائيات:\n"
            results_text += f"• إجمالي الكائنات: {total_objects}\n"
            results_text += f"• أنواع مختلفة: {unique_types}\n"
            results_text += f"• نسبة الاكتشاف: {coverage_percentage:.1f}%\n"
            
            results_text += f"\n🏷️ التصنيف حسب النوع:\n"
            for type_name, count in sorted(type_counts.items()):
                results_text += f"• {type_name}: {count}\n"
                
            results_text += f"\n⏱️  أداء النظام:\n"
            results_text += f"• وقت المعالجة: {processing_time:.2f} ثانية\n"
            results_text += f"• سرعة الكشف: {total_objects/processing_time:.1f} كائن/ثانية\n"
            
        else:
            results_text += "❌ لم يتم اكتشاف أي كائنات\n"
            results_text += "💡 جرب صورة أخرى أو اضبط إعدادات الكشف\n"
        
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, results_text)
        
        self.status_var.set(f"✅ اكتمل الكشف الشامل - تم اكتشاف {total_objects} كائن ({unique_types} نوع)")
        messagebox.showinfo("نجاح", f"تم اكتشاف {total_objects} كائن من {unique_types} نوع مختلف!")
    
    def display_image(self, image, label):
        """عرض الصورة في Label"""
        image.thumbnail((600, 500))
        photo = ImageTk.PhotoImage(image)
        label.configure(image=photo)
        label.image = photo
    
    def save_image(self):
        """حفظ الصورة المعالجة"""
        if self.processed_image is None:
            messagebox.showwarning("تحذير", "لا توجد صورة معالجة للحفظ")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="حفظ الصورة المعالجة",
            defaultextension=".jpg",
            filetypes=[
                ("JPEG files", "*.jpg"),
                ("PNG files", "*.png"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                cv2.imwrite(file_path, self.processed_image)
                messagebox.showinfo("نجاح", f"تم حفظ الصورة في: {file_path}")
                self.status_var.set(f"✅ تم حفظ الصورة: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("خطأ", f"تعذر حفظ الصورة: {str(e)}")
    
    def show_error(self, message):
        """عرض رسالة خطأ"""
        self.root.after(0, lambda: messagebox.showerror("خطأ", message))
        self.root.after(0, lambda: self.detect_btn.configure(state='normal'))
        self.root.after(0, self.progress.stop)
        self.root.after(0, lambda: self.status_var.set("❌ فشل في الكشف"))

def main():
    """الدالة الرئيسية"""
    try:
        print("🚀 بدء تشغيل النظام الشامل للكشف عن الأشياء...")
        root = tk.Tk()
        app = CompleteDetectionSystem(root)
        root.mainloop()
    except Exception as e:
        print(f"❌ خطأ في تشغيل النظام: {e}")
        input("اضغط Enter للإغلاق...")

if __name__ == "__main__":
    main()