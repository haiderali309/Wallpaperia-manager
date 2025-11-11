from firebase_admin import db

class FirebaseService:
    
    @staticmethod
    def get_ref(path='wallpapers'):
        return db.reference(path)
    
    # Category Operations
    @staticmethod
    def get_categories():
        ref = FirebaseService.get_ref('wallpapers/Categories')
        return ref.get() or {}
    
    @staticmethod
    def add_category(category_id, name, c_url):
        ref = FirebaseService.get_ref(f'wallpapers/Categories/{category_id}')
        ref.set({
            'name': name,
            'C_url': c_url,
            'wallpapers': []
        })
        return True
    
    @staticmethod
    def update_category(category_id, name, c_url):
        ref = FirebaseService.get_ref(f'wallpapers/Categories/{category_id}')
        data = ref.get()
        if data:
            data['name'] = name
            data['C_url'] = c_url
            ref.set(data)
            return True
        return False
    
    @staticmethod
    def delete_category(category_id):
        ref = FirebaseService.get_ref(f'wallpapers/Categories/{category_id}')
        ref.delete()
        return True
    
    # Wallpaper Operations (within categories)
    @staticmethod
    def add_wallpaper_to_category(category_id, wallpaper_url):
        ref = FirebaseService.get_ref(f'wallpapers/Categories/{category_id}/wallpapers')
        wallpapers = ref.get() or []
        wallpapers.append(wallpaper_url)
        ref.set(wallpapers)
        return True
    
    @staticmethod
    def remove_wallpaper_from_category(category_id, wallpaper_url):
        ref = FirebaseService.get_ref(f'wallpapers/Categories/{category_id}/wallpapers')
        wallpapers = ref.get() or []
        if wallpaper_url in wallpapers:
            wallpapers.remove(wallpaper_url)
            ref.set(wallpapers)
            return True
        return False
    
    # Static Category Operations (Animated, Art, Nature, etc.)
    @staticmethod
    def get_static_category(category_name):
        ref = FirebaseService.get_ref(f'wallpapers/{category_name}')
        return ref.get() or []
    
    @staticmethod
    def add_wallpaper_to_static(category_name, wallpaper_url):
        ref = FirebaseService.get_ref(f'wallpapers/{category_name}')
        wallpapers = ref.get() or []
        wallpapers.append(wallpaper_url)
        ref.set(wallpapers)
        return True
    
    @staticmethod
    def remove_wallpaper_from_static(category_name, wallpaper_url):
        ref = FirebaseService.get_ref(f'wallpapers/{category_name}')
        wallpapers = ref.get() or []
        if wallpaper_url in wallpapers:
            wallpapers.remove(wallpaper_url)
            ref.set(wallpapers)
            return True
        return False
    
    @staticmethod
    def get_all_data():
        ref = FirebaseService.get_ref('wallpapers')
        return ref.get() or {}