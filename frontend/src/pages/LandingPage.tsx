import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';

export default function LandingPage() {
  const navigate = useNavigate();
  const [showTagline, setShowTagline] = useState(false);

  const auroraText = "AURORA";
  const letters = auroraText.split('');

  // Show tagline after title animation completes
  useEffect(() => {
    const timer = setTimeout(() => {
      setShowTagline(true);
    }, 2000); // Delay for letter animations to complete
    return () => clearTimeout(timer);
  }, []);

  // Animation variants for dropping letters
  const letterVariants = {
    initial: {
      y: -500,
      opacity: 0,
      rotateZ: -45
    },
    animate: {
      y: 0,
      opacity: 1,
      rotateZ: 0,
      transition: {
        type: "spring",
        damping: 12,
        stiffness: 200,
        duration: 0.8
      }
    }
  };

  // Tagline animation variants
  const taglineVariants = {
    initial: {
      opacity: 0,
      y: 20
    },
    animate: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.8,
        ease: "easeOut"
      }
    }
  };

  // Button animation variants
  const buttonVariants = {
    initial: {
      opacity: 0,
      scale: 0.8
    },
    animate: {
      opacity: 1,
      scale: 1,
      transition: {
        delay: 0.3,
        duration: 0.5,
        ease: "easeOut"
      }
    },
    hover: {
      scale: 1.05,
      boxShadow: "0 20px 40px rgba(59, 130, 246, 0.4)"
    },
    tap: {
      scale: 0.95
    }
  };

  // Floating particles animation
  const particleVariants = {
    animate: {
      y: [0, -30, 0],
      x: [0, 15, 0],
      opacity: [0.3, 0.7, 0.3],
      transition: {
        duration: 6,
        repeat: Infinity,
        ease: "easeInOut"
      }
    }
  };

  const scrollToFeatures = () => {
    document.getElementById('features')?.scrollIntoView({
      behavior: 'smooth'
    });
  };

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Animated Aurora Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900">
        <motion.div
          className="absolute inset-0 opacity-50"
          animate={{
            background: [
              "radial-gradient(circle at 20% 50%, rgba(168, 85, 247, 0.4) 0%, transparent 50%)",
              "radial-gradient(circle at 80% 50%, rgba(59, 130, 246, 0.4) 0%, transparent 50%)",
              "radial-gradient(circle at 50% 80%, rgba(16, 185, 129, 0.4) 0%, transparent 50%)",
              "radial-gradient(circle at 50% 20%, rgba(236, 72, 153, 0.4) 0%, transparent 50%)",
              "radial-gradient(circle at 20% 50%, rgba(168, 85, 247, 0.4) 0%, transparent 50%)"
            ]
          }}
          transition={{
            duration: 10,
            repeat: Infinity,
            ease: "linear"
          }}
        />
      </div>

      {/* Floating Particles */}
      {[...Array(20)].map((_, i) => (
        <motion.div
          key={i}
          className="absolute w-2 h-2 bg-white rounded-full"
          style={{
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
          }}
          variants={particleVariants}
          animate="animate"
          transition={{
            delay: i * 0.2,
            duration: 4 + Math.random() * 4
          }}
        />
      ))}

      {/* Main Content */}
      <div className="container mx-auto px-4 py-16 relative z-10">
        {/* Hero Section */}
        <div className="min-h-screen flex flex-col items-center justify-center text-center">
          {/* Animated AURORA Title */}
          <div className="mb-8 flex justify-center items-center space-x-1">
            {letters.map((letter, index) => (
              <motion.span
                key={index}
                variants={letterVariants}
                initial="initial"
                animate="animate"
                transition={{
                  delay: index * 0.15, // Stagger effect
                }}
                className="text-8xl md:text-9xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 inline-block"
                style={{
                  textShadow: "0 0 30px rgba(168, 85, 247, 0.5)"
                }}
              >
                {letter}
              </motion.span>
            ))}
          </div>

          {/* Animated Tagline */}
          {showTagline && (
            <motion.div
              variants={taglineVariants}
              initial="initial"
              animate="animate"
              className="mb-12"
            >
              <p className="text-2xl md:text-3xl text-blue-200 font-light tracking-wide">
                Audit Object Recognition & Analytics
              </p>
              <p className="text-lg md:text-xl text-purple-300 mt-2">
                Indonesian Tax Object Classifier with AI
              </p>
            </motion.div>
          )}

          {/* CTA Buttons */}
          {showTagline && (
            <motion.div
              variants={buttonVariants}
              initial="initial"
              animate="animate"
              className="flex flex-col sm:flex-row gap-4 justify-center mb-12"
            >
              <motion.button
                variants={buttonVariants}
                whileHover="hover"
                whileTap="tap"
                onClick={() => navigate('/sign-up')}
                className="px-10 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-semibold text-lg shadow-xl"
              >
                Get Started
              </motion.button>

              <motion.button
                variants={buttonVariants}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={scrollToFeatures}
                className="px-10 py-4 bg-white/10 backdrop-blur-lg text-white rounded-lg font-semibold text-lg border border-white/20 hover:bg-white/20"
              >
                Learn More
              </motion.button>
            </motion.div>
          )}

          {/* Scroll Indicator */}
          {showTagline && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 1, duration: 1 }}
              className="absolute bottom-10"
            >
              <motion.div
                animate={{ y: [0, 10, 0] }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  ease: "easeInOut"
                }}
                className="text-white/50 cursor-pointer"
                onClick={scrollToFeatures}
              >
                <svg
                  className="w-6 h-6 mx-auto"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 14l-7 7m0 0l-7-7m7 7V3"
                  />
                </svg>
              </motion.div>
            </motion.div>
          )}
        </div>

        {/* Features Section */}
        <motion.div
          id="features"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 1 }}
          className="py-24"
        >
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="text-4xl md:text-5xl font-bold text-white text-center mb-16"
          >
            Why Choose AURORA?
          </motion.h2>

          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {[
              {
                title: 'Accurate',
                description: 'AI-powered classification with high precision',
                icon: '🎯',
                delay: 0
              },
              {
                title: 'Fast',
                description: 'Process thousands of entries in seconds',
                icon: '⚡',
                delay: 0.2
              },
              {
                title: 'Explainable',
                description: 'Transparent AI decisions you can trust',
                icon: '🔍',
                delay: 0.4
              }
            ].map((feature, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 50 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{
                  delay: feature.delay,
                  duration: 0.6,
                  type: "spring",
                  stiffness: 100
                }}
                whileHover={{
                  scale: 1.05,
                  y: -10,
                  transition: { duration: 0.2 }
                }}
                className="bg-white/10 backdrop-blur-lg p-8 rounded-xl border border-white/20 hover:bg-white/20 transition-all"
              >
                <div className="text-5xl mb-4">{feature.icon}</div>
                <h3 className="text-2xl font-bold text-white mb-3">
                  {feature.title}
                </h3>
                <p className="text-blue-200 text-lg">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
}
