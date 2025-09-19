import pretty_midi
import random

instrument_names = {
    "melody": "Electric Guitar (clean)",
    "harmony": "Pad 1 (new age)",
}

folk_scales = {
    "major_pentatonic": [0, 2, 4, 7, 9],
    "minor_pentatonic": [0, 3, 5, 7, 10],
}

lyrics = [
    "Aarambh Hai Prachand", "Bolein Mastakon Ke Jhund", "Aaj Jung Ki Ghadi Ki Tum Guhaar Do",
    "Aan Baan Shaan", "Ya Ki Jaan Ka Ho Daan", "Aaj Ek Dhanush Ke Baan Pe Utaar Do",
    "Man Kare So Pran De", "Jo Man Kare So Pran Le", "Wo Wahi To Ek Sarv Shaktimaan Hai",
    "Krishn Ki Pukaar Hai Ye", "Bhaagwat Ka Saar Hai", "Ki Yuddh Hi To Veer Ka Pramaan Hai",
    "Kaurawon Ki Bheed Ho", "Ya Paandavon Ka Neer(D) Ho", "Jo Lad Sakaa Hai Wohi To Mahaan Hai",
    "Jeet Ki Hawas Nahi", "Kisi Pe Koi Vash Nahi", "Kya Zindagi Hai Thokaron Pe Maar Do",
    "Maut Ant Hai Nahi", "To Maut Se Bhi Kyun Darein", "Ye Jaake Aasmaano Mein Dahaad Do!",
    "Wo Dayaa Ka Bhaav Yaki", "Shaurya Ka Chunaav Yaki", "Haar Ka Wo Ghaav Tum Ye Soch Lo",
    "Yaki Bhoore Bhaal Par", "Jalaa Rahe Vijay Ka Laal", "Laal Ye GULAAL Tum Ye Soch Lo",
    "Rang Kesari Ho Ya Mridang Kesari Ho", "Ya Ki Kesari Ho Taal Tum Ye Soch Lo",
    "Jis Kavi Ki Kalpana Mein", "Zindagi Ho Prem Geet", "Us Kavi Ko Aaj Tum Nakaar Do",
    "Bheegti Maso Mein Aaj", "Phoolti Ragon Mein Aaj", "Aag Ki Lapat Ka Tum Bhaghaar Do"
]

def generate_melody(scale, length=8):
    melody = []
    for _ in range(length):
        note = random.choice(scale) + 60
        melody.append(note)
    return melody

def create_modern_arrangement(scale_name, lyrics, save_as="folk_song_modern.mid"):
    print(f"Arranging folk song in {scale_name} scale with lyrics...")
    
    if scale_name not in folk_scales:
        raise ValueError(f"Scale '{scale_name}' not found in supported scales.")
    
    midi = pretty_midi.PrettyMIDI()
    scale = folk_scales[scale_name]
    note_duration = 0.5
    
    # CHANGE 1: Generate 80 notes for a 40-second song
    melody_notes = generate_melody(scale, length=80) 
    
    guitar_program = pretty_midi.instrument_name_to_program(instrument_names["melody"])
    guitar = pretty_midi.Instrument(program=guitar_program)
    
    current_time = 0.0
    for i, pitch in enumerate(melody_notes):
        note = pretty_midi.Note(
            velocity=100, pitch=pitch, start=current_time, end=current_time + note_duration
        )
        guitar.notes.append(note)
        
        # CHANGE 2: Loop the lyrics to fit the longer melody
        lyric_text = lyrics[i % len(lyrics)] 
        midi.lyrics.append(pretty_midi.Lyric(text=lyric_text, time=current_time))
        
        current_time += note_duration
    midi.instruments.append(guitar)

    pad_program = pretty_midi.instrument_name_to_program(instrument_names["harmony"])
    pad = pretty_midi.Instrument(program=pad_program)
    
    for i in range(0, len(melody_notes), 4):
        start_time = i * note_duration
        root_note = scale[0] + 48
        chord_notes = [root_note, root_note + 4, root_note + 7]
        for pitch in chord_notes:
            note = pretty_midi.Note(
                velocity=60, pitch=pitch, start=start_time, end=start_time + (note_duration * 4)
            )
            pad.notes.append(note)
    midi.instruments.append(pad)

    drums = pretty_midi.Instrument(program=0, is_drum=True)
    
    for i in range(0, len(melody_notes), 2):
        kick_start = i * note_duration
        kick = pretty_midi.Note(velocity=100, pitch=36, start=kick_start, end=kick_start + 0.1)
        drums.notes.append(kick)
        
        snare_start = (i + 1) * note_duration
        if snare_start < current_time:
            snare = pretty_midi.Note(velocity=90, pitch=38, start=snare_start, end=snare_start + 0.1)
            drums.notes.append(snare)
    midi.instruments.append(drums)

    midi.write(save_as)
    print(f"Modern arrangement with lyrics saved as '{save_as}'.")

if __name__ == "__main__":
    output_file_path = r"C:\Users\badam giridhar\Desktop\python\folk_song_with_lyrics.mid"
    create_modern_arrangement("major_pentatonic", lyrics, save_as=output_file_path)