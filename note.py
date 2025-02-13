from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import json
import os

class NotesApp(App):
    def build(self):
        # Main layout
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        self.main_layout.add_widget(Label(
            text='My Notes',
            size_hint_y=None,
            height=50,
            font_size=24
        ))
        
        # Note input area
        self.note_input = TextInput(
            hint_text='Write your note here...',
            size_hint=(1, None),
            height=100,
            multiline=True
        )
        self.main_layout.add_widget(self.note_input)
        
        # Save button
        save_button = Button(
            text='Save Note',
            size_hint=(1, None),
            height=50,
            background_color=(0.2, 0.7, 0.3, 1)
        )
        save_button.bind(on_press=self.save_note)
        self.main_layout.add_widget(save_button)
        
        # Scroll view for notes list
        scroll = ScrollView(size_hint=(1, 1))
        self.notes_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=5
        )
        self.notes_layout.bind(minimum_height=self.notes_layout.setter('height'))
        scroll.add_widget(self.notes_layout)
        self.main_layout.add_widget(scroll)
        
        # Load existing notes
        self.load_notes()
        
        return self.main_layout
    
    def save_note(self, instance):
        if self.note_input.text.strip():
            # Create note container
            note_container = BoxLayout(
                size_hint_y=None,
                height=100,
                spacing=5
            )
            
            # Note text
            note_text = TextInput(
                text=self.note_input.text,
                multiline=True,
                readonly=True
            )
            
            # Delete button
            delete_button = Button(
                text='Delete',
                size_hint_x=0.2,
                background_color=(0.8, 0.2, 0.2, 1)
            )
            delete_button.bind(on_press=lambda x: self.delete_note(note_container))
            
            note_container.add_widget(note_text)
            note_container.add_widget(delete_button)
            
            # Add to layout
            self.notes_layout.add_widget(note_container)
            
            # Clear input
            self.note_input.text = ''
            
            # Save to file
            self.save_notes_to_file()
    
    def delete_note(self, note_container):
        self.notes_layout.remove_widget(note_container)
        self.save_notes_to_file()
    
    def save_notes_to_file(self):
        notes = []
        for child in self.notes_layout.children:
            note_text = child.children[1].text  # TextInput is the second child
            notes.append(note_text)
        
        with open('notes.json', 'w') as f:
            json.dump(notes, f)
    
    def load_notes(self):
        try:
            if os.path.exists('notes.json'):
                with open('notes.json', 'r') as f:
                    notes = json.load(f)
                
                for note in notes:
                    # Create note container
                    note_container = BoxLayout(
                        size_hint_y=None,
                        height=100,
                        spacing=5
                    )
                    
                    # Note text
                    note_text = TextInput(
                        text=note,
                        multiline=True,
                        readonly=True
                    )
                    
                    # Delete button
                    delete_button = Button(
                        text='Delete',
                        size_hint_x=0.2,
                        background_color=(0.8, 0.2, 0.2, 1)
                    )
                    delete_button.bind(on_press=lambda x: self.delete_note(note_container))
                    
                    note_container.add_widget(note_text)
                    note_container.add_widget(delete_button)
                    
                    self.notes_layout.add_widget(note_container)
        except:
            pass

if __name__ == '__main__':
    NotesApp().run()
