import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import os
import webbrowser
import subprocess
import sys
import re
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import threading

class YouTubeUploaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Uploader - UPLOADAJA.ID")
        self.root.geometry("600x680")
        self.root.resizable(False, False)
        
        # Set custom icon if available
        self.set_custom_icon()
        
        # Configure clean white theme
        self.setup_clean_theme()
        
        # Variables
        self.token_path = tk.StringVar()
        self.token_save_path = tk.StringVar()
        self.client_secret_path = tk.StringVar()
        self.video_path = tk.StringVar()
        self.thumbnail_path = tk.StringVar()
        self.custom_metadata_enabled = tk.BooleanVar()
        self.selected_category = tk.StringVar(value="22")  # Default to People & Blogs
        
        # YouTube categories
        self.youtube_categories = {
            "1": "Film & Animation",
            "2": "Autos & Vehicles", 
            "10": "Music",
            "15": "Pets & Animals",
            "17": "Sports",
            "19": "Travel & Events",
            "20": "Gaming",
            "22": "People & Blogs",
            "23": "Comedy",
            "24": "Entertainment",
            "25": "News & Politics",
            "26": "Howto & Style",
            "27": "Education",
            "28": "Science & Technology"
        }
        
        # OAuth scopes
        self.SCOPES = [
            "https://www.googleapis.com/auth/youtube.force-ssl",
            "https://www.googleapis.com/auth/youtube",
            "https://www.googleapis.com/auth/youtube.readonly",
            "https://www.googleapis.com/auth/youtube.upload"
        ]
        
        self.setup_ui()
    
    def set_custom_icon(self):
        """Set a custom icon for the application"""
        try:
            # Use the water-drops.ico file
            if os.path.exists("water-drops.ico"):
                self.root.iconbitmap("water-drops.ico")
            elif os.path.exists("icon.ico"):
                self.root.iconbitmap("icon.ico")
        except Exception as e:
            # If icon setting fails, just continue without icon
            pass
    
    def setup_clean_theme(self):
        # Configure the style for clean white theme
        style = ttk.Style()
        
        # Configure colors
        bg_color = "#ffffff"
        fg_color = "#333333"
        button_bg = "#f0f0f0"
        entry_bg = "#ffffff"
        accent_color = "#0078d4"
        
        # Configure root window
        self.root.configure(bg=bg_color)
        
        # Configure ttk styles
        style.theme_use('clam')
        
        # Configure frame style
        style.configure('Clean.TFrame', background=bg_color, relief='flat')
        style.configure('Section.TFrame', background=bg_color, relief='flat', borderwidth=0)
        
        # Configure label style
        style.configure('Clean.TLabel', 
                       background=bg_color, 
                       foreground=fg_color,
                       font=('Segoe UI', 9))
        
        # Configure title label style
        style.configure('Title.TLabel', 
                       background=bg_color, 
                       foreground=accent_color,
                       font=('Segoe UI', 14, 'bold'))
        
        # Configure section header style
        style.configure('Header.TLabel', 
                       background=bg_color, 
                       foreground=accent_color,
                       font=('Segoe UI', 10, 'bold'))
        
        # Configure copyright style
        style.configure('Copyright.TLabel', 
                       background=bg_color, 
                       foreground='#666666',
                       font=('Segoe UI', 8))
        
        # Configure button style
        style.configure('Clean.TButton',
                       background=button_bg,
                       foreground=fg_color,
                       borderwidth=1,
                       focuscolor='none',
                       font=('Segoe UI', 9))
        style.map('Clean.TButton',
                 background=[('active', '#e1e1e1'),
                           ('pressed', '#d0d0d0')])
        
        # Configure entry style
        style.configure('Clean.TEntry',
                       fieldbackground=entry_bg,
                       background=entry_bg,
                       foreground=fg_color,
                       borderwidth=1,
                       insertcolor=fg_color,
                       font=('Segoe UI', 9))
        
        # Configure combobox style
        style.configure('Clean.TCombobox',
                       fieldbackground=entry_bg,
                       background=entry_bg,
                       foreground=fg_color,
                       borderwidth=1,
                       font=('Segoe UI', 9))
        
        # Configure checkbutton style
        style.configure('Clean.TCheckbutton',
                       background=bg_color,
                       foreground=fg_color,
                       focuscolor='none',
                       font=('Segoe UI', 9))
        
        # Configure separator style
        style.configure('Clean.TSeparator',
                       background='#cccccc')
        
    def setup_ui(self):
        # Main frame with clean theme
        main_frame = ttk.Frame(self.root, padding="10", style='Clean.TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        row = 0
        
        # Title
        title_label = ttk.Label(main_frame, text="YouTube Video Uploader", style='Title.TLabel')
        title_label.grid(row=row, column=0, columnspan=3, pady=(0, 10))
        row += 1
        
        # === AUTHENTICATION SECTION ===
        auth_frame = ttk.Frame(main_frame, style='Section.TFrame', padding="5")
        auth_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 5))
        auth_frame.columnconfigure(1, weight=1)
        
        ttk.Label(auth_frame, text="Authentication", style='Header.TLabel').grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))
        
        # Client secret file selection
        ttk.Label(auth_frame, text="Client Secret:", style='Clean.TLabel').grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(auth_frame, textvariable=self.client_secret_path, width=40, style='Clean.TEntry').grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 5))
        ttk.Button(auth_frame, text="Browse", command=self.browse_client_secret_file, style='Clean.TButton').grid(row=1, column=2)
        
        # Token save path for generation
        ttk.Label(auth_frame, text="Save Token to:", style='Clean.TLabel').grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(auth_frame, textvariable=self.token_save_path, width=40, style='Clean.TEntry').grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(5, 5))
        ttk.Button(auth_frame, text="Browse", command=self.browse_token_save_path, style='Clean.TButton').grid(row=2, column=2)
        
        # Token.json file selection
        ttk.Label(auth_frame, text="Token file:", style='Clean.TLabel').grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Entry(auth_frame, textvariable=self.token_path, width=40, style='Clean.TEntry').grid(row=3, column=1, sticky=(tk.W, tk.E), padx=(5, 5))
        ttk.Button(auth_frame, text="Browse", command=self.browse_token_file, style='Clean.TButton').grid(row=3, column=2)
        
        # Action buttons
        button_frame = ttk.Frame(auth_frame, style='Clean.TFrame')
        button_frame.grid(row=4, column=0, columnspan=3, pady=(5, 0))
        ttk.Button(button_frame, text="Generate Token", command=self.generate_token, style='Clean.TButton').pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Refresh Token", command=self.refresh_token, style='Clean.TButton').pack(side=tk.LEFT)
        
        row += 1
        
        # === VIDEO UPLOAD SECTION ===
        video_frame = ttk.Frame(main_frame, style='Section.TFrame', padding="5")
        video_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 5))
        video_frame.columnconfigure(1, weight=1)
        
        ttk.Label(video_frame, text="Video Upload", style='Header.TLabel').grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))
        
        # Video file selection
        ttk.Label(video_frame, text="Video file:", style='Clean.TLabel').grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(video_frame, textvariable=self.video_path, width=40, style='Clean.TEntry').grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 5))
        ttk.Button(video_frame, text="Browse", command=self.browse_video_file, style='Clean.TButton').grid(row=1, column=2)
        
        # Thumbnail file selection
        ttk.Label(video_frame, text="Thumbnail (optional):", style='Clean.TLabel').grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(video_frame, textvariable=self.thumbnail_path, width=40, style='Clean.TEntry').grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(5, 5))
        ttk.Button(video_frame, text="Browse", command=self.browse_thumbnail_file, style='Clean.TButton').grid(row=2, column=2)
        
        # YouTube category
        ttk.Label(video_frame, text="Category:", style='Clean.TLabel').grid(row=3, column=0, sticky=tk.W, pady=2)
        category_combo = ttk.Combobox(video_frame, textvariable=self.selected_category, width=37, style='Clean.TCombobox')
        category_combo['values'] = [f"{k}: {v}" for k, v in self.youtube_categories.items()]
        category_combo.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=(5, 5))
        category_combo.set("22: People & Blogs")  # Default selection
        
        row += 1
        
        # === METADATA SECTION ===
        metadata_frame = ttk.Frame(main_frame, style='Section.TFrame', padding="5")
        metadata_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 5))
        metadata_frame.columnconfigure(1, weight=1)
        
        ttk.Label(metadata_frame, text="Metadata", style='Header.TLabel').grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))
        
        # Custom metadata toggle
        ttk.Checkbutton(metadata_frame, text="Enable custom title and tags", 
                       variable=self.custom_metadata_enabled,
                       command=self.toggle_custom_metadata, style='Clean.TCheckbutton').grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))
        
        # Custom title input (initially disabled)
        ttk.Label(metadata_frame, text="Title:", style='Clean.TLabel').grid(row=2, column=0, sticky=tk.W, pady=2)
        self.title_entry = ttk.Entry(metadata_frame, width=40, state='disabled', style='Clean.TEntry')
        self.title_entry.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # Custom tags input (initially disabled)
        ttk.Label(metadata_frame, text="Tags (comma separated):", style='Clean.TLabel').grid(row=3, column=0, sticky=tk.W, pady=2)
        self.tags_entry = ttk.Entry(metadata_frame, width=40, state='disabled', style='Clean.TEntry')
        self.tags_entry.grid(row=3, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # Description input (initially disabled)
        ttk.Label(metadata_frame, text="Description:", style='Clean.TLabel').grid(row=4, column=0, sticky=(tk.W, tk.N), pady=2)
        self.description_text = scrolledtext.ScrolledText(metadata_frame, width=40, height=3, state='disabled',
                                                         bg="#ffffff", fg="#333333", insertbackground="#333333",
                                                         selectbackground="#0078d4", selectforeground="#ffffff",
                                                         font=('Segoe UI', 9), wrap=tk.WORD)
        self.description_text.grid(row=4, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=(5, 0), pady=2)
        
        row += 1
        
        # === ACTION BUTTONS ===
        buttons_frame = ttk.Frame(main_frame, style='Clean.TFrame')
        buttons_frame.grid(row=row, column=0, columnspan=3, pady=(0, 5))
        
        ttk.Button(buttons_frame, text="Generate Metadata", command=self.generate_metadata, style='Clean.TButton').pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="Upload Video", command=self.upload_video, style='Clean.TButton').pack(side=tk.LEFT)
        
        row += 1
        
        # === STATUS LOG SECTION ===
        status_frame = ttk.Frame(main_frame, style='Section.TFrame', padding="5")
        status_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(1, weight=1)
        
        ttk.Label(status_frame, text="Status Log", style='Header.TLabel').grid(row=0, column=0, sticky=tk.W, pady=(0, 3))
        
        self.status_text = scrolledtext.ScrolledText(status_frame, width=60, height=6, state='disabled',
                                                    bg="#f8f8f8", fg="#333333", insertbackground="#333333",
                                                    selectbackground="#0078d4", selectforeground="#ffffff",
                                                    font=('Consolas', 8), wrap=tk.WORD)
        self.status_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Bind click event for hyperlinks
        self.status_text.bind("<Button-1>", self.on_status_click)
        
        row += 1
        
        # === COPYRIGHT SECTION ===
        copyright_frame = ttk.Frame(main_frame, style='Clean.TFrame')
        copyright_frame.grid(row=row, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Label(copyright_frame, text="© 2024 Hendri - UPLOADAJA.ID", style='Copyright.TLabel').pack()
        
        # Set default paths if files exist
        if os.path.exists("token.json"):
            self.token_path.set("token.json")
        if os.path.exists("client_secret.json"):
            self.client_secret_path.set("client_secret.json")
        # Set default token save path
        self.token_save_path.set("token.json")
            
    def browse_token_file(self):
        filename = filedialog.askopenfilename(
            title="Select token.json file",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.token_path.set(filename)
            
    def browse_client_secret_file(self):
        filename = filedialog.askopenfilename(
            title="Select client_secret.json file",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.client_secret_path.set(filename)
    
    def browse_token_save_path(self):
        filename = filedialog.asksaveasfilename(
            title="Save token.json as",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.token_save_path.set(filename)
            
    def browse_video_file(self):
        filename = filedialog.askopenfilename(
            title="Select video file",
            filetypes=[("Video files", "*.mp4 *.mov *.mkv *.webm *.avi"), ("All files", "*.*")]
        )
        if filename:
            self.video_path.set(filename)
    
    def browse_thumbnail_file(self):
        filename = filedialog.askopenfilename(
            title="Select thumbnail image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp"), ("All files", "*.*")]
        )
        if filename:
            self.thumbnail_path.set(filename)
            
    def toggle_custom_metadata(self):
        if self.custom_metadata_enabled.get():
            self.title_entry.config(state='normal')
            self.tags_entry.config(state='normal')
            self.description_text.config(state='normal')
        else:
            self.title_entry.config(state='disabled')
            self.tags_entry.config(state='disabled')
            self.description_text.config(state='disabled')
    
    def log_status(self, message):
        self.status_text.config(state='normal')
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state='disabled')
        self.root.update()
    
    def on_status_click(self, event):
        # Get the position of the click
        index = self.status_text.index(f"@{event.x},{event.y}")
        line_start = self.status_text.index(f"{index} linestart")
        line_end = self.status_text.index(f"{index} lineend")
        line_text = self.status_text.get(line_start, line_end)
        
        # Check if the line contains a URL
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, line_text)
        
        if urls:
            # Open the first URL found in the line
            webbrowser.open(urls[0])
    
    def upload_thumbnail(self, youtube, video_id, thumbnail_path):
        """Upload thumbnail for the video"""
        if not os.path.exists(thumbnail_path):
            self.log_status(f"⚠️ Thumbnail not found: {thumbnail_path}")
            return False

        try:
            self.log_status("Uploading thumbnail...")
            request = youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(thumbnail_path)
            )
            response = request.execute()
            self.log_status(f"🖼️ Thumbnail uploaded successfully!")
            return True
        except Exception as e:
            self.log_status(f"⚠️ Failed to upload thumbnail: {str(e)}")
            return False
    
    def generate_token(self):
        if not self.client_secret_path.get() or not os.path.exists(self.client_secret_path.get()):
            messagebox.showerror("Error", "Please select a client_secret.json file first")
            return
        
        if not self.token_save_path.get():
            messagebox.showerror("Error", "Please specify where to save the token.json file")
            return
        
        try:
            self.log_status("Starting OAuth flow...")
            self.log_status("A browser window will open for authentication.")
            
            # Create OAuth flow
            flow = InstalledAppFlow.from_client_secrets_file(
                self.client_secret_path.get(), self.SCOPES
            )
            
            # Run the OAuth flow
            creds = flow.run_local_server(port=0)
            
            # Save the token
            with open(self.token_save_path.get(), "w") as token:
                token.write(creds.to_json())
            
            # Auto-load the generated token path
            self.token_path.set(self.token_save_path.get())
            
            self.log_status(f"Token generated and saved to: {self.token_save_path.get()}")
            self.log_status("Token file automatically loaded for use.")
            messagebox.showinfo("Success", "Token generated successfully!")
            
        except Exception as e:
            error_msg = f"Error generating token: {str(e)}"
            self.log_status(error_msg)
            messagebox.showerror("Error", error_msg)
            
    def refresh_token(self):
        if not self.token_path.get():
            messagebox.showerror("Error", "Please select a token.json file first")
            return
            
        try:
            self.log_status("Refreshing token...")
            
            # Load credentials
            creds = Credentials.from_authorized_user_file(
                self.token_path.get(), 
                scopes=self.SCOPES
            )
            
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
                
                # Save refreshed token
                with open(self.token_path.get(), 'w') as token:
                    token.write(creds.to_json())
                    
                self.log_status("Token refreshed successfully!")
                messagebox.showinfo("Success", "Token refreshed successfully!")
            else:
                self.log_status("Token is still valid.")
                messagebox.showinfo("Info", "Token is still valid.")
                
        except Exception as e:
            error_msg = f"Error refreshing token: {str(e)}"
            self.log_status(error_msg)
            messagebox.showerror("Error", error_msg)
            
    def generate_metadata(self):
        try:
            # Get category ID from selection
            category_selection = self.selected_category.get()
            category_id = category_selection.split(":")[0] if ":" in category_selection else "22"
            
            # Get description and handle newlines properly
            description = self.description_text.get("1.0", tk.END).strip()
            # Replace actual newlines with \n for JSON, but keep them as newlines for YouTube
            description = description.replace('\r\n', '\n').replace('\r', '\n')
            
            # Get tags
            tags = []
            if self.custom_metadata_enabled.get() and self.tags_entry.get().strip():
                tags = [tag.strip() for tag in self.tags_entry.get().split(",") if tag.strip()]
            
            # Create metadata
            metadata = {
                "description": description,
                "tags": tags,
                "categoryId": category_id,
                "defaultLanguage": "en",
                "defaultAudioLanguage": "en"
            }
            
            # Save metadata.json
            with open("metadata.json", "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
                
            self.log_status("Metadata.json generated successfully!")
            messagebox.showinfo("Success", "Metadata.json generated successfully!")
            
        except Exception as e:
            error_msg = f"Error generating metadata: {str(e)}"
            self.log_status(error_msg)
            messagebox.showerror("Error", error_msg)
            
    def get_authenticated_service(self):
        if not self.token_path.get() or not os.path.exists(self.token_path.get()):
            raise Exception("Token file not found")
            
        if not self.client_secret_path.get() or not os.path.exists(self.client_secret_path.get()):
            raise Exception("Client secret file not found")
            
        creds = Credentials.from_authorized_user_file(
            self.token_path.get(), 
            self.SCOPES
        )
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                with open(self.token_path.get(), "w") as token:
                    token.write(creds.to_json())
            else:
                raise Exception("Invalid credentials. Please refresh token first.")
                
        return build("youtube", "v3", credentials=creds)
        
    def load_metadata(self):
        if os.path.exists("metadata.json"):
            with open("metadata.json", "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            # Generate metadata if it doesn't exist
            self.generate_metadata()
            with open("metadata.json", "r", encoding="utf-8") as f:
                return json.load(f)
                
    def upload_video_thread(self):
        try:
            if not self.video_path.get() or not os.path.exists(self.video_path.get()):
                raise Exception("Please select a valid video file")
                
            self.log_status("Starting video upload...")
            
            # Get authenticated service
            youtube = self.get_authenticated_service()
            
            # Load metadata
            metadata = self.load_metadata()
            
            # Get video title
            file_name = os.path.basename(self.video_path.get())
            if self.custom_metadata_enabled.get() and self.title_entry.get().strip():
                title = self.title_entry.get().strip()
            else:
                title = os.path.splitext(file_name)[0]
                
            # Prepare request body
            request_body = {
                "snippet": {
                    "title": title,
                    "description": metadata["description"],
                    "tags": metadata["tags"],
                    "categoryId": metadata["categoryId"],
                    "defaultLanguage": metadata["defaultLanguage"],
                    "defaultAudioLanguage": metadata["defaultAudioLanguage"]
                },
                "status": {
                    "privacyStatus": "private",
                    "selfDeclaredMadeForKids": False,
                    "embeddable": False
                }
            }
            
            # Create media upload
            media = MediaFileUpload(
                self.video_path.get(), 
                chunksize=-1, 
                resumable=True, 
                mimetype="video/*"
            )
            
            # Create upload request
            request = youtube.videos().insert(
                part="snippet,status",
                body=request_body,
                media_body=media
            )
            
            # Upload with progress
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    self.log_status(f"Uploading {file_name}... {progress}%")
                    
            video_id = response['id']
            self.log_status(f"✅ Upload complete! Video ID: {video_id}")
            self.log_status(f"🔗 Video URL: https://www.youtube.com/watch?v={video_id}")
            
            # Upload thumbnail if provided
            if self.thumbnail_path.get() and os.path.exists(self.thumbnail_path.get()):
                self.upload_thumbnail(youtube, video_id, self.thumbnail_path.get())
            else:
                self.log_status("ℹ️ No thumbnail provided - skipping thumbnail upload")
            
            messagebox.showinfo("Success", f"Video uploaded successfully!\nVideo ID: {video_id}")
            
        except Exception as e:
            error_msg = f"Upload failed: {str(e)}"
            self.log_status(error_msg)
            messagebox.showerror("Error", error_msg)
            
    def upload_video(self):
        # Run upload in separate thread to prevent GUI freezing
        upload_thread = threading.Thread(target=self.upload_video_thread)
        upload_thread.daemon = True
        upload_thread.start()

def main():
    root = tk.Tk()
    app = YouTubeUploaderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
