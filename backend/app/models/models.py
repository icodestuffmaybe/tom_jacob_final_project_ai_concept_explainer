from sqlalchemy import Column, String, Integer, Text, DateTime, Float, Boolean, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class Student(Base):
    __tablename__ = 'students'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    grade_level = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime)
    preferences = Column(JSON)
    
    learning_sessions = relationship("LearningSession", back_populates="student")
    progress_records = relationship("Progress", back_populates="student")

class Concept(Base):
    __tablename__ = 'concepts'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    subject = Column(String)
    description = Column(Text)
    prerequisites = Column(JSON)
    related_topics = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    learning_sessions = relationship("LearningSession", back_populates="concept")
    progress_records = relationship("Progress", back_populates="concept")

class LearningSession(Base):
    __tablename__ = 'learning_sessions'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    student_id = Column(String, ForeignKey('students.id'))
    concept_id = Column(String, ForeignKey('concepts.id'))
    query = Column(Text)
    explanation = Column(Text)
    sources = Column(JSON)
    svg_diagrams = Column(JSON)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    student = relationship("Student", back_populates="learning_sessions")
    concept = relationship("Concept", back_populates="learning_sessions")
    quizzes = relationship("Quiz", back_populates="session")

class Quiz(Base):
    __tablename__ = 'quizzes'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    session_id = Column(String, ForeignKey('learning_sessions.id'))
    questions = Column(JSON)
    student_responses = Column(JSON)
    score = Column(Float)
    mastery_achieved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    session = relationship("LearningSession", back_populates="quizzes")

class Progress(Base):
    __tablename__ = 'progress'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    student_id = Column(String, ForeignKey('students.id'))
    concept_id = Column(String, ForeignKey('concepts.id'))
    mastery_level = Column(Float)
    attempts = Column(Integer)
    last_reviewed = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student", back_populates="progress_records")
    concept = relationship("Concept", back_populates="progress_records")