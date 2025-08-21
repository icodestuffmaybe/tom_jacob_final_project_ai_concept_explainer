import React from 'react'

interface SVGFlashcardProps {
  svgContent: string
}

const SVGFlashcard: React.FC<SVGFlashcardProps> = ({ svgContent }) => {
  if (!svgContent) {
    return (
      <div className="zen-card rounded-lg p-8 text-center">
        <div className="text-gray-400">
          <span className="text-4xl mb-4 block">🎨</span>
          <p>Visual flashcard will appear here</p>
          <p className="text-sm mt-2">Processing visual representation...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="zen-card rounded-lg p-4 max-w-4xl mx-auto">
      <div 
        className="rounded-lg overflow-hidden shadow-lg"
        dangerouslySetInnerHTML={{ __html: svgContent }}
      />
      
      <div className="mt-4 text-center">
        <p className="text-sm text-gray-400">
          ✨ AI-generated visual explanation using the Feynman technique
        </p>
      </div>
    </div>
  )
}

export default SVGFlashcard