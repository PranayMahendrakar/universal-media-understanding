#!/usr/bin/env python3
"""
Universal Media Understanding Platform
Author: Pranay M.

System that comprehends and contextualizes all forms of human media
throughout history.
"""

import ollama
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.prompt import Prompt
import json
import sys

console = Console()

BANNER = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║            📺 UNIVERSAL MEDIA UNDERSTANDING PLATFORM 📺                        ║
║                    Cross-Historical Media Intelligence                         ║
║                           Author: Pranay M.                                    ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

MODULES = {
    "1": ("Media Format Analyzer", "format", "Analyze media formats"),
    "2": ("Historical Context Engine", "historical", "Provide historical context"),
    "3": ("Narrative Decoder", "narrative", "Decode media narratives"),
    "4": ("Symbolism Interpreter", "symbolism", "Interpret media symbolism"),
    "5": ("Cultural Impact Assessor", "cultural", "Assess cultural impact"),
    "6": ("Media Evolution Tracker", "evolution", "Track media evolution"),
    "7": ("Cross-Media Connector", "cross_media", "Connect related media"),
    "8": ("Audience Analyzer", "audience", "Analyze intended audiences"),
    "9": ("Influence Mapper", "influence", "Map media influences"),
    "10": ("Media Dashboard", "dashboard", "View media intelligence dashboard")
}

SYSTEM_PROMPTS = {
    "format": """You are an expert in media formats and their characteristics.

For each media format analysis, examine:

1. **Format Identification**: Type of media, technical specs
2. **Format History**: Origins and evolution of format
3. **Affordances**: What format enables/constrains
4. **Production Context**: How media was created
5. **Distribution Methods**: How it reached audiences
6. **Preservation Status**: Archival considerations

Analyze media formats comprehensively.""",

    "historical": """You are an expert in media history and historical context.

For each historical context request, provide:

1. **Time Period**: When media was created
2. **Historical Events**: Relevant contemporary events
3. **Social Context**: Society at the time
4. **Technology Context**: Available technologies
5. **Cultural Movements**: Relevant artistic/cultural trends
6. **Reception History**: How it was received then vs now

Provide historical context for media.""",

    "narrative": """You are an expert in narrative analysis and storytelling.

For each narrative decoding, analyze:

1. **Story Structure**: Plot, arc, pacing
2. **Character Analysis**: Characters, roles, development
3. **Themes**: Major and minor themes
4. **Point of View**: Perspective and framing
5. **Subtext**: Hidden meanings, implications
6. **Narrative Devices**: Techniques used

Decode media narratives thoroughly.""",

    "symbolism": """You are an expert in semiotics and symbolic interpretation.

For each symbolism interpretation, identify:

1. **Visual Symbols**: Images, colors, compositions
2. **Verbal Symbols**: Words, names, phrases
3. **Structural Symbols**: Form, format, arrangement
4. **Cultural Symbols**: Culture-specific meanings
5. **Universal Symbols**: Cross-cultural meanings
6. **Symbol Evolution**: How meanings have changed

Interpret media symbolism comprehensively.""",

    "cultural": """You are an expert in media studies and cultural impact.

For each cultural impact assessment, evaluate:

1. **Contemporary Impact**: Immediate effects
2. **Long-term Legacy**: Lasting influence
3. **Cultural Change**: What it changed in society
4. **Discourse Effects**: What conversations it sparked
5. **Imitation/Influence**: What it inspired
6. **Controversy**: Debates it generated

Assess cultural impact of media.""",

    "evolution": """You are an expert in media history and evolution.

For each media evolution tracking, document:

1. **Origins**: Where this type began
2. **Key Developments**: Major milestones
3. **Technological Changes**: How tech shaped evolution
4. **Format Transitions**: Medium changes
5. **Current State**: Present form
6. **Future Trajectory**: Where it's heading

Track evolution of media forms.""",

    "cross_media": """You are an expert in intertextuality and media connections.

For each cross-media connection, identify:

1. **Direct References**: Explicit connections
2. **Influences**: What influenced what
3. **Adaptations**: Cross-medium versions
4. **Thematic Links**: Shared themes
5. **Formal Links**: Shared techniques
6. **Network Mapping**: Connection web

Connect related media across formats and time.""",

    "audience": """You are an expert in audience analysis and media reception.

For each audience analysis, examine:

1. **Intended Audience**: Who it was made for
2. **Actual Audience**: Who consumed it
3. **Audience Expectations**: What audiences expected
4. **Reception Patterns**: How different groups received it
5. **Fan Cultures**: Communities around media
6. **Audience Evolution**: How audiences changed

Analyze media audiences and reception.""",

    "influence": """You are an expert in media influence and power.

For each influence mapping, analyze:

1. **Immediate Influence**: Direct effects on other works
2. **Stylistic Influence**: Aesthetic impacts
3. **Cultural Influence**: Broader cultural effects
4. **Political Influence**: Political implications
5. **Economic Influence**: Industry effects
6. **Influence Networks**: Chains of influence

Map media influence patterns.""",

    "dashboard": """You are an expert in media analytics and intelligence.

For each dashboard, generate:

1. **Media Overview**: Content being analyzed
2. **Context Summary**: Historical and cultural context
3. **Narrative Insights**: Story and meaning analysis
4. **Cultural Impact**: Significance assessment
5. **Connection Map**: Related media network
6. **Key Insights**: Most important findings

View media understanding dashboard."""
}

def get_multiline_input(prompt_text):
    console.print(f"\n[cyan]{prompt_text}[/cyan]")
    console.print("[dim](Type 'END' on a new line when finished)[/dim]\n")
    lines = []
    while True:
        try:
            line = input()
            if line.strip().upper() == 'END':
                break
            lines.append(line)
        except EOFError:
            break
    return '\n'.join(lines)

def query_llama(system_prompt, user_input):
    try:
        response = ollama.chat(model='llama3.2', messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_input}
        ])
        return response['message']['content']
    except Exception as e:
        return f"Error: {str(e)}\n\nMake sure Ollama is running."

def display_menu():
    console.print(BANNER, style="bold blue")
    table = Table(title="📺 Media Understanding Modules", show_header=True, header_style="bold magenta")
    table.add_column("Option", style="cyan", width=8)
    table.add_column("Module", style="green", width=28)
    table.add_column("Description", style="white", width=42)
    for key, (name, _, desc) in MODULES.items():
        table.add_row(key, name, desc)
    table.add_row("0", "Exit", "Exit the application")
    console.print(table)

def run_module(module_key):
    name, key, desc = MODULES[module_key]
    console.print(Panel(f"📺 {name}", style="bold green"))
    user_input = get_multiline_input(f"Describe your {name.lower()} request:")
    with console.status(f"[bold green]Processing {name}..."):
        response = query_llama(SYSTEM_PROMPTS[key], user_input)
    console.print(Panel(Markdown(response), title=f"📺 {name} Results", border_style="green"))

def main():
    while True:
        display_menu()
        choice = Prompt.ask("\nSelect a module", choices=["0","1","2","3","4","5","6","7","8","9","10"])
        if choice == "0":
            console.print("\n[yellow]Thank you for using the Universal Media Understanding Platform![/yellow]")
            console.print("[dim]Author: Pranay M.[/dim]\n")
            break
        try:
            run_module(choice)
        except KeyboardInterrupt:
            console.print("\n[yellow]Operation cancelled.[/yellow]")
        except Exception as e:
            console.print(f"\n[red]Error: {str(e)}[/red]")
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
