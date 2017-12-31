import datetime
from lxml import etree

# Collection of quotes from Miyamoto Musashi and Sun Tzu (kept short for SVG display)
QUOTES = {
    'musashi': [
        "Do nothing which is of no use.",
        "Accept death resolutely.",
        "Perceive what cannot be seen.",
        "Think light of self, deep of world.",
        "Practice makes art useful anytime.",
        "Fight as you practice.",
        "Study the universe, not one planet.",
        "The aim is not to use force.",
        "Control self to control others.",
        "Keep the mind always flowing."
    ],
    'sun_tzu': [
        "Supreme art is subduing without fighting.",
        "Break resistance without battle.",
        "Greatest victory needs no war.",
        "Know your enemy and yourself.",
        "Win first, then go to war.",
        "The art of war is vital.",
        "In chaos lies opportunity.",
        "Appear weak when strong.",
        "Subdue without fighting.",
        "Know when to fight and when not to."
    ]
}

def get_rotating_quote(test_mode=False):
    """
    Returns a quote that rotates every 3 hours based on the current time.
    Alternates between Musashi and Sun Tzu quotes.
    All quotes are kept short for simple single-line display.
    
    Args:
        test_mode: If True, forces a different quote for testing
    """
    if test_mode:
        # Force a different quote for testing (switch from current Sun Tzu to Musashi)
        author = 'musashi'
        author_name = 'Musashi'
        quote_index = 0  # Use first quote
    else:
        current_hour = datetime.datetime.now().hour
        # Change quote every 3 hours (0-2, 3-5, 6-8, 9-11, 12-14, 15-17, 18-20, 21-23)
        time_slot = current_hour // 3
        
        # Alternate between authors based on time slot
        if time_slot % 2 == 0:
            author = 'musashi'
            author_name = 'Musashi'
        else:
            author = 'sun_tzu'
            author_name = 'Sun Tzu'
        
        # Use time slot to select quote (ensures same quote for 3 hours)
        quote_index = time_slot % len(QUOTES[author])
    
    quote = QUOTES[author][quote_index]
    return f'"{quote}" ~ {author_name}'

def update_svg_quote(filename, quote_data):
    """
    Updates the quote in the specified SVG file
    Targeted replacement within the Quote&Purpose section only
    """
    try:
        # Read the file content
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and replace the specific quote line in the Quote&Purpose section
        # Look for the pattern: class="cc">.  "quote" ~ Author</tspan>
        import re
        
        # More specific pattern that targets the exact structure
        pattern = r'(class="cc">\.  )"[^"]*" ~ (Musashi|Sun Tzu)(</tspan>)'
        
        if re.search(pattern, content):
            # Replace just the quote part, keeping the structure intact
            new_content = re.sub(pattern, rf'\1{quote_data}\3', content)
            
            # Write back to file
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✓ Updated quote in {filename}")
        else:
            print(f"✗ Could not find quote pattern in {filename}")
            
    except Exception as e:
        print(f"✗ Error updating {filename}: {e}")

def show_all_quotes():
    """
    Display all available quotes from both authors
    """
    print("\n📚 All Available Quotes:")
    print("=" * 50)
    
    print("\n🗡️  Musashi Quotes:")
    for i, quote in enumerate(QUOTES['musashi']):
        print(f"  {i+1:2d}. {quote}")
    
    print("\n⚔️  Sun Tzu Quotes:")
    for i, quote in enumerate(QUOTES['sun_tzu']):
        print(f"  {i+1:2d}. {quote}")
    
    print("=" * 50)

def test_all_quotes():
    """
    Test function to cycle through all quotes sequentially
    """
    print("🧪 Testing all quotes sequentially...")
    
    for author in ['musashi', 'sun_tzu']:
        author_name = 'Musashi' if author == 'musashi' else 'Sun Tzu'
        print(f"\n📖 Testing {author_name} quotes:")
        
        for i, quote in enumerate(QUOTES[author]):
            test_quote = f'"{quote}" ~ {author_name}'
            print(f"  {i+1:2d}. {test_quote}")
            
            # Update SVG files with this quote
            update_svg_quote('dark_mode.svg', test_quote)
            update_svg_quote('light_mode.svg', test_quote)
            
            # Small delay to see the change
            import time
            time.sleep(1)
    
    print("\n✅ All quotes tested! Check your SVG files.")

def main():
    """
    Main function to rotate quotes and update SVG files
    """
    print("🔄 Rotating quotes from Miyamoto Musashi and Sun Tzu...")
    
    # Show all available quotes first
    show_all_quotes()
    
    # Ask user what they want to do
    print("\n" + "=" * 50)
    print("Choose an option:")
    print("1. Run normal time-based rotation")
    print("2. Test all quotes sequentially")
    print("3. Force next quote (bypass time)")
    
    try:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "2":
            test_all_quotes()
            return
        elif choice == "3":
            # Force next quote for testing
            current_quote = get_rotating_quote(test_mode=True)
            print(f"\n📝 Forced quote: {current_quote}")
        else:
            # Normal time-based rotation
            current_quote = get_rotating_quote()
            print(f"\n📝 Current quote: {current_quote}")
        
        # Update both SVG files
        update_svg_quote('dark_mode.svg', current_quote)
        update_svg_quote('light_mode.svg', current_quote)
        
        print("✅ Quote rotation complete!")
        
        # Show when the next quote change will occur
        current_hour = datetime.datetime.now().hour
        next_change_hour = ((current_hour // 3) + 1) * 3
        if next_change_hour >= 24:
            next_change_hour = 0
            next_change_time = f"tomorrow at {next_change_hour:02d}:00"
        else:
            next_change_time = f"at {next_change_hour:02d}:00"
        
        print(f"⏰ Next quote change: {next_change_time}")
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == '__main__':
    main()