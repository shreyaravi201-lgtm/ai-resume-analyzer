import pytest
from roadmap_generator import generate_roadmap

def test_generate_roadmap_empty():
    roadmap = generate_roadmap([])
    assert len(roadmap) == 1
    assert "Continuous Enhancement" in roadmap[0]["topic"]
    assert "match all required skills" in roadmap[0]["activity"]

def test_generate_roadmap_with_missing():
    missing_skills = ["FastAPI", "Docker", "SuperFancyNewTool"]
    roadmap = generate_roadmap(missing_skills)
    
    assert len(roadmap) == 3
    assert roadmap[0]["week"] == "Week 1"
    assert "FastAPI" in roadmap[0]["topic"]
    assert "modern web APIs" in roadmap[0]["activity"]
    
    assert roadmap[1]["week"] == "Week 2"
    assert "Docker" in roadmap[1]["topic"]
    assert "Containerize applications" in roadmap[1]["activity"]
    
    # Check fallback for unknown tool
    assert roadmap[2]["week"] == "Week 3"
    assert "SuperFancyNewTool" in roadmap[2]["topic"]
    assert "Master SuperFancyNewTool by reviewing official documentation" in roadmap[2]["activity"]
