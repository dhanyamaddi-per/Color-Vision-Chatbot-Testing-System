import tkinter as tk
from tkinter import messagebox, Button
import spacy
import subprocess
import re
import random

# Download spaCy model (one-time execution)
subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])  # Using "en_core_web_sm" for efficiency

user_name = None
pattern_responses = [
    (r"types|kinds", [
        "There are several types of color blindness, including red-green color blindness and blue-yellow color blindness.",
        "Common types of color blindness include protanopia, deuteranopia, and tritanopia."]),
    (r"red-green color blindness", [
        "Red-green color blindness is the most common type, affecting how people perceive reds and greens. There are variations within this category, such as protanopia (weakness in red perception) and deuteranopia (weakness in green perception).",
        "Many people with color blindness have difficulty distinguishing between reds and greens. This can be caused by protanopia, deuteranopia, or other variations of red-green color blindness."]),
    (r"blue-yellow color blindness", [
        "Blue-yellow color blindness, also known as tritanopia, is a less common type where people have trouble differentiating between blues and yellows. It can make distinguishing certain colors in twilight or under colored lighting difficult.",
        "Tritanopia, or blue-yellow color blindness, affects how someone perceives blue and yellow hues. This can make tasks like reading traffic lights or interpreting color-coded information challenging."]),
    (r"tests|diagnosed", [
        "There are various tests for color blindness, including the Ishihara color vision test and the Farnsworth-Munsell 100 hue test. I can provide you one for Red Green color blindness, click on the Red Green Test button to take test.",
        "Color blindness tests like Ishihara color vision test help diagnose color vision deficiencies.I can provide you one for Red Green color blindness, click on the Red Green Test button to take test."]),
    (r"treatment|cure", [
        "Currently, there is no cure for color blindness. However, some aids and tools can help people with color vision deficiency distinguish colors better.",
        "Treatment options for color blindness are limited, but researchers are exploring gene therapy and other interventions."]),
    (r"cause(s)?", [
        "Color blindness can arise from two main causes:\n 1) Inherited genetic defects in the cone cells of the retina responsible for color vision, and \n "
        "2) Damage to the eye, optic nerve, or parts of the brain responsible for processing color information.",
        "There are two main reasons for color blindness: either genetic faults in the retina's cone cells, or damage to the eye, optic nerve, or brain areas that handle color processing."]),
    (r"occupations|professions", [
        "Color blindness can impact job opportunities and career choices in some professions that require precise differentiation of colors. Here are some examples: \n Transportation: \n "
        "Pilots, air traffic controllers, and drivers of commercial vehicles all rely on colored lights, markings, and signals for safe navigation.\nEmergency Services: "
        "\nFirefighters depend on color coding on equipment to identify tools and respond quickly.\nPolice officers may use colored flares or markings at crime scenes."
        "\nSkilled Trades: \n Electricians work with color-coded wires to ensure proper connections, and plumbers rely on color coding to identify hot and cold water lines.\n"
        "Design and Manufacturing: \nGraphic designers use color extensively for visual communication, and quality control inspectors in some industries rely on color coding to identify defects."]),
     (r"living with color blindness", [
        "Living with color blindness involves making adjustments in daily life, such as using color-coded labels and relying on patterns and textures.",
        "People with color blindness can lead fulfilling lives by using adaptive strategies and seeking support when needed."]),
    (r"(?!color blindness\b)(?:affect.*daily life|daily life.*affect)", [
        "Color blindness can affect daily life in various ways, such as difficulty in distinguishing traffic lights, reading maps, and identifying certain foods.",
        "The impact of color blindness on daily activities depends on the severity and type of color vision deficiency."]),
    (r"examples",[
        "Color blindness can impact daily activities in various ways. For instance, distinguishing traffic lights, matching clothes, or reading colored maps can be difficult. Some people might also struggle with ripeness cues of fruits and vegetables based on color.",
        "Imagine trying to pick out ripe tomatoes from a bowl of green and red ones, or matching a blue shirt with a pair of black pants that appear very similar to you. These are some everyday challenges faced by color-blind individuals."]),
    (r"prevalence", [
        "Color blindness is more common in men than in women. It affects approximately 8% of men and 0.5% of women of Northern European descent.",
        "The prevalence of color blindness varies among different populations and ethnicities."]),
    (r"inherited|genetic", [
        "Yes, color blindness is often inherited genetically. It is passed down through the X chromosome, which is why it is more common in men.",
        "Yes, genetic factors play a significant role in the development of color vision deficiency."]),
    (r"(?:impact.*career|career.*impact)", [
        "The impact of color blindness on a person's career depends on the specific job requirements. Some professions may have restrictions for color-blind individuals.",
        "Certain occupations, such as pilots or electricians, may require color vision testing as part of the hiring process."]),
    (r"challenges", [
        "Some challenges of color blindness include difficulties in certain occupations, limitations in perceiving art or design, and potential safety hazards.",
        "Color blindness can pose challenges in everyday tasks, such as driving, cooking, and choosing clothing.",
        "Beyond the physical limitations, color blindness can sometimes lead to social or emotional challenges. Feeling excluded from activities that rely heavily on color vision or misunderstood by others can be frustrating. However, with increased awareness and support, these challenges can be addressed."]),
    (r"tools", [
        "There are various tools and resources available for color-blind individuals, such as color-blind-friendly apps, special glasses, and accessible design guidelines.",
        "Technology has made significant advancements in providing solutions for color vision deficiencies, including mobile apps and digital accessibility features."]),
    (r"glasses", ["Color-blind glasses , also known as color-enhancing glasses like EnChroma Cx30, Hilux, can help individuals with color vision deficiency distinguish colors more effectively.",
                       "Specialized glasses for color blindness like EnChroma Cx30, Hilux use filters to adjust color perception and enhance the visibility of certain hues."]),
    (r"awareness", [
        "Color blindness awareness initiatives aim to educate people about the condition, promote accessibility and inclusion, and reduce stigma associated with color vision deficiency.",
        "Raising awareness about color blindness can help create a more inclusive society and improve support for individuals with color vision deficiencies."]),
    (r"advancements in research", [
        "Researchers are continuously working on advancements in color blindness treatments, gene therapy, and assistive technologies to improve the quality of life for color-blind individuals.",
        "Recent breakthroughs in genetics and biotechnology have opened up new possibilities for treating color vision deficiencies."]),
    (r"art(ist)?", [
        "Color blindness can influence how individuals perceive and create art. Some artists with color blindness develop unique styles or use alternative techniques to express themselves.",
        "Artists with color vision deficiencies may rely on contrast, texture, and form to convey their artistic vision.",
        "An artist with color blindness, don't perceive the full spectrum of colors that others do. But that can also be a source of creativity! One focuses more on shapes, values (light and dark), and textures to create one's art. There's a whole world of expression beyond just color.",
        "Sure, I can share some insights on a color-blind artist. While they might not see all the colors others do, it allows them to experiment with unique color combinations and focus on composition and light. Many famous artists throughout history have had some form of color blindness."]),
    (r"color blindness simulation", [
        "Color blindness simulators are tools that allow individuals to experience how color-blind individuals perceive the world. They can be helpful in promoting empathy and understanding.",
        "Using color blindness simulators can help raise awareness about the challenges faced by color-blind individuals in daily life."]),
    (r"vision accessibility", [
        "Vision accessibility refers to designing products, environments, and technologies to be inclusive and accessible to individuals with visual impairments, including color blindness.",
        "Creating vision-accessible designs benefits not only color-blind individuals but also people with other visual impairments."]),
    (r"workplace accommodations", [
        "Workplace accommodations for color-blind individuals may include using color-blind-friendly charts and diagrams, providing alternative labeling methods, and ensuring accessible digital interfaces.",
        "Employers can support color-blind employees by implementing inclusive policies, providing training on color vision deficiency, and offering assistive technologies."]),
    (r"sports|atheletes", [
        "Color blindness can pose challenges in certain sports, such as soccer or tennis, where distinguishing between team colors or tracking fast-moving objects may be important.",
        "Athletes with color vision deficiencies may need to rely on other cues, such as player positions or field markings, to navigate the game effectively."]),
    (r"education", [
        "In education, teachers can support color-blind students by using alternative teaching materials, providing verbal descriptions of visual content, and creating accessible learning environments.",
        "Educators play a crucial role in ensuring that students with color vision deficiencies have equal access to educational resources and opportunities."]),
    (r"color blindness", [
        "Color blindness, also known as color vision deficiency, is a condition where a person has difficulty distinguishing certain colors. It affects how individuals perceive colors."]),
    (r"thank\s?you", [
        "No Worries! I'm happy I was able to assist you.",
        "I'm happy I could assist you."]),
    (r"(cannot|unable).*?(find|identify).*?(color\s?)",[
        "Would you like to learn more about color blindness or try a color blindness test? You may also use the Identify Color button to identify some basic colors.",
        "There are tools and resources available to help individuals with color blindness navigate their surroundings.You may also use the Identify Color button to identify some basic colors."])
]


# Shuffle the pattern-response pairs
random.shuffle(pattern_responses)


def greet_user():
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, "Bella: Hi there! Welcome. I'm Bella, your friendly chatbot for color blindness.\n")
    speak("Hi there! Welcome. I'm Bella, your friendly chatbot for color blindness.")
    chat_history.config(state=tk.DISABLED)
    chat_history.see(tk.END)  # Scroll to the bottom of the chat history
    user_entry.focus_set()  # focus on the entry field for easy typing

def speak(text):
    chat_history.update_idletasks()  # Update the chat area to ensure text is displayed
    chat_history.after(100, lambda: subprocess.call(["say", text]))

def greet_and_ask_name():
    greet_user()
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, "Bella: What's your name? Please give your full name.\n")
    speak("What's your name? Please give your full name.")
    chat_history.config(state=tk.DISABLED)


def get_name_from_input(input_text):
    global user_name
    nlp = spacy.load('en_core_web_sm')
    input_text = input_text.title()  # Capitalize first letter of each word
    input_text = input_text.replace('I\'M', '')  # replacing i'm with empty string as it is not being handled by doc.ents
    doc = nlp(input_text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":  # check if NER is person to identify name
            user_name = ent.text
            return True
    return False


def run_blind_test_gui():
    subprocess.call(["python", "test.py"])
    messagebox.showinfo("Blind Test", "Color Blind Test is done.")


def identify_color():
    subprocess.call(["python", "identify_c.py"])
    messagebox.showinfo("Blind Test", "I hope you were able to recognize the colors that you couldn't.")


def confirm_quit():
    confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to quit?")
    if confirmation:
        root.destroy()


def send_message():
    user_input = user_entry.get()
    user_entry.delete(0, tk.END)  # Clear the input field
    if not user_input:
        messagebox.showinfo("Error", "Please type something.")
        return

    if user_input.lower() in ['quit', 'bye', 'exit']:
        confirm_quit()
        return

    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, f"You: {user_input}\n")

    if not user_name:
        get_name_from_input(user_input)
        if user_name:
            chat_history.insert(tk.END, f"Bella: Nice to meet you, {user_name}! How can I help you today?\n")
            speak(f"Nice to meet you, {user_name}! How can I help you today?")
        else:
            chat_history.insert(tk.END, "Bella: I couldn't find your name. Can you tell me again?\n")
            speak("I couldn't find your name. Can you tell me again?")
    else:
        # Add responses based on user input
        # Check for pattern matches and select a random response
        matched_response = None
        for pattern_response in pattern_responses:
            if len(pattern_response) != 2:
                print("Invalid pattern-response pair:", pattern_response)
                continue  # Skip this pair and move to the next one
            pattern, responses = pattern_response
            if re.search(pattern, user_input, re.IGNORECASE):
                matched_response = random.choice(responses)
                break

                # If no pattern matched, provide a default response
        if not matched_response:
            chat_history.insert(tk.END, f"Bella: Hi {user_name}, how can I help you today?\n")
            speak("Hi {user_name}, how can I help you today?")
        else:
            chat_history.insert(tk.END, f"Bella: {matched_response}\n")
            speak(matched_response)

    chat_history.config(state=tk.DISABLED)
    chat_history.see(tk.END)  # Scroll to the bottom of the chat history


# Create the GUI window
root = tk.Tk()
root.title("Chatbot for color blindness")

# Chat history display
chat_history = tk.Text(root, state=tk.DISABLED)
chat_history.pack(expand=True, fill=tk.BOTH)

# User input field
user_entry = tk.Entry(root)
user_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
user_entry.bind("<Return>", send_message)  # Send message on Enter key press

# Send button (optional, for users who prefer clicking)
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(side=tk.LEFT)

# **Ensure greeting on startup**
greet_and_ask_name()

# Blind test button
blind_test_button = Button(root, text="Red Green Test", command=run_blind_test_gui)
blind_test_button.pack()

# Color detection button
color_detection_button = Button(root, text="Identify Color", command=identify_color)
color_detection_button.pack()

# Start the GUI event loop
root.mainloop()
