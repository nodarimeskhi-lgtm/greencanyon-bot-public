"use client";

import { motion } from "framer-motion";
import Image from "next/image";

// A premium serif font for headers, using Tailwind's default serif or we can load a specific one via next/font
export default function Home() {
  return (
    <main className="min-h-screen bg-[#FDFBF7] text-[#2C332A] selection:bg-[#4A5D4E]/30 overflow-x-hidden font-sans">
      
      {/* Navigation - Elegant Light Mode */}
      <motion.nav 
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 1 }}
        className="absolute top-0 w-full z-50 px-6 xl:px-12 py-8 flex justify-between items-center"
      >
        <div className="flex flex-col text-white">
           <span className="text-[10px] tracking-[0.3em] uppercase opacity-90">Eco Village</span>
           <span className="text-xl tracking-widest font-light">GREEN<span className="font-medium">CANYON</span></span>
        </div>
        <div className="hidden md:flex gap-10 text-xs tracking-[0.2em] font-medium uppercase text-white drop-shadow-md">
          <a href="#about" className="hover:text-amber-100 transition-colors">ჩვენს შესახებ</a>
          <a href="#infrastructure" className="hover:text-amber-100 transition-colors">ინფრასტრუქტურა</a>
          <a href="#investments" className="hover:text-amber-100 transition-colors">ინვესტიციები</a>
          <a href="#projects" className="hover:text-amber-100 transition-colors">პროექტები</a>
        </div>
      </motion.nav>

      {/* Hero Section */}
      <section className="relative h-screen w-full flex items-center justify-center">
         <motion.div 
            initial={{ scale: 1.05, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 1.5, ease: "easeOut" }}
            className="absolute inset-0 z-0"
         >
           {/* Replace this src with the actual canyon photo from Wix */}
           <img
             src="https://images.unsplash.com/photo-1549474744-8cb3897103ba?q=80&w=2574&auto=format&fit=crop"
             alt="Tsalka Canyon Nature"
             className="w-full h-full object-cover"
           />
           <div className="absolute inset-0 bg-[#2C332A]/30 mix-blend-multiply" />
         </motion.div>

         <div className="relative z-10 text-center px-4 max-w-5xl mx-auto flex flex-col items-center mt-20 text-white">
            <motion.h2 
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ duration: 1, delay: 0.8 }}
              className="tracking-[0.4em] text-xs md:text-sm uppercase mb-6 font-medium text-amber-50"
            >
              Eco Village & Resort • 1600m Altitude
            </motion.h2>
            
            <motion.h1 
              initial={{ y: 30, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ duration: 1.2, delay: 1 }}
              className="text-5xl md:text-7xl lg:text-8xl font-serif font-light tracking-wide mb-8 leading-[1.1] text-[#FDFBF7]"
            >
              ბუნებასთან ჰარმონიის <br/><span className="italic font-light">ახალი სტანდარტი</span>
            </motion.h1>
            
            <motion.p 
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ duration: 1, delay: 1.3 }}
              className="text-[#FDFBF7] text-lg md:text-xl font-light max-w-2xl mb-12 opacity-95 leading-relaxed drop-shadow-sm"
            >
              ყველაზე სწრაფად მზარდი ტურისტული ლოკაცია საქართველოში. ეკოტურიზმის ახალი მარგალიტი 200 000+ ვიზიტორით წელიწადში.
            </motion.p>
            
            <motion.a 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 1, delay: 1.6 }}
              href="#about" 
              className="px-10 py-4 bg-[#FDFBF7]/90 backdrop-blur-sm text-[#2C332A] text-xs uppercase tracking-[0.2em] font-semibold hover:bg-white hover:scale-105 transition-all duration-300"
            >
              აღმოაჩინე
            </motion.a>
         </div>
      </section>

      {/* Intro & Investment Snapshot */}
      <section id="about" className="py-24 px-6 lg:px-12 bg-[#FDFBF7] text-center">
        <motion.div 
          initial={{ y: 40, opacity: 0 }}
          whileInView={{ y: 0, opacity: 1 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 1 }}
          className="max-w-4xl mx-auto"
        >
          <h2 className="text-[#4A5D4E] tracking-[0.2em] text-sm uppercase mb-6 font-medium">ეკო-სისტემა</h2>
          <p className="text-3xl md:text-4xl font-serif text-[#2C332A] leading-relaxed mb-16">
            Green Canyon Eco Village არ არის უბრალოდ კომპლექსი, ეს არის პრემიუმ კლასის ეკო-სისტემა. ინტეგრირებული მსოფლიო კლასის მენეჯმენტით და უმაღლესი სერტიფიკატებით 1600 მეტრის სიმაღლეზე.
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12 border-t border-[#4A5D4E]/20 pt-16">
            <div>
              <div className="text-5xl font-serif text-[#4A5D4E] mb-4">14%</div>
              <h4 className="text-xs tracking-widest uppercase font-bold text-[#2C332A] mb-2">Projected ROI</h4>
              <p className="text-sm font-light text-gray-600">მაღალი და სტაბილური წლიური უკუგება საერთაშორისო მენეჯმენტის პირობებში.</p>
            </div>
            <div>
              <div className="text-5xl font-serif text-[#4A5D4E] mb-4">5★</div>
              <h4 className="text-xs tracking-widest uppercase font-bold text-[#2C332A] mb-2">მსოფლიო მენეჯმენტი</h4>
              <p className="text-sm font-light text-gray-600">ინფრასტრუქტურის სამართავად მიმდინარეობს მოლაპარაკებები 5-ვარსკვლავიან ბრენდთან.</p>
            </div>
            <div>
              <div className="text-5xl font-serif text-[#4A5D4E] mb-4">30%</div>
              <h4 className="text-xs tracking-widest uppercase font-bold text-[#2C332A] mb-2">Capital Growth</h4>
              <p className="text-sm font-light text-gray-600">მშენებლობის დასრულებისას თქვენი ქონების ღირებულების გარანტირებული ზრდა.</p>
            </div>
          </div>
        </motion.div>
      </section>

      {/* Architecture & Eco Standards */}
      <section id="infrastructure" className="py-24 px-6 lg:px-12 bg-[#F3F0E9]">
        <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          <motion.div 
            initial={{ x: -40, opacity: 0 }}
            whileInView={{ x: 0, opacity: 1 }}
            viewport={{ once: true, margin: "-100px" }}
            transition={{ duration: 1 }}
            className="flex flex-col justify-center order-2 lg:order-1"
          >
            <h3 className="text-[#4A5D4E] tracking-[0.2em] text-xs uppercase mb-6 font-medium">მდგრადობა და ინჟინერია</h3>
            <h2 className="text-4xl md:text-5xl font-serif mb-8 leading-tight text-[#2C332A]">
              ჩვენ არ ვერგებით კლიმატს,<br /> 
              <span className="italic text-[#4A5D4E]">ჩვენ ვმართავთ მას ეკოლოგიურად</span>
            </h2>
            <p className="text-gray-600 font-light text-lg mb-12 leading-relaxed">
              მთის ბუნებაში ცხოვრება არ ნიშნავს კომფორტის დათმობას. თითოეული ნაგებობა შექმნილია მძიმე კლიმატური პირობებისთვის, სრული თერმული ავტონომიითა და უმაღლესი ხარისხით.
            </p>
            
            <div className="space-y-8">
              <div className="flex gap-4 items-start">
                <div className="w-8 h-8 rounded-full border border-[#4A5D4E] flex items-center justify-center text-[#4A5D4E] shrink-0">1</div>
                <div>
                  <h4 className="text-lg font-bold text-[#2C332A] mb-2">საერთაშორისო სერტიფიკატები</h4>
                  <p className="text-sm text-gray-600 leading-relaxed font-light">პროექტის დაგეგმარება და მშენებლობა მიმდინარეობს <strong className="font-semibold text-[#2C332A]">LEED Gold (აშშ)</strong> და <strong className="font-semibold text-[#2C332A]">Green Globe</strong> სტანდარტების მოპოვების მიზნით.</p>
                </div>
              </div>
              <div className="flex gap-4 items-start">
                <div className="w-8 h-8 rounded-full border border-[#4A5D4E] flex items-center justify-center text-[#4A5D4E] shrink-0">2</div>
                <div>
                  <h4 className="text-lg font-bold text-[#2C332A] mb-2">WoodCastor თერმული ავტონომია</h4>
                  <p className="text-sm text-gray-600 leading-relaxed font-light">მაღალი სტანდარტის <strong className="font-semibold text-[#2C332A]">200 მმ-იანი თბოიზოლაცია</strong> და სამმაგი ენერგოეფექტური მინაპაკეტი აბსოლუტურად გამორიცხავს სითბოს დანაკარგს.</p>
                </div>
              </div>
              <div className="flex gap-4 items-start">
                <div className="w-8 h-8 rounded-full border border-[#4A5D4E] flex items-center justify-center text-[#4A5D4E] shrink-0">3</div>
                <div>
                  <h4 className="text-lg font-bold text-[#2C332A] mb-2">ბრიტანული კლიმატ-კომფორტი</h4>
                  <p className="text-sm text-gray-600 leading-relaxed font-light">გათბობა-გაგრილების სისტემები უზრუნველყოფილია ჩვენი პარტნიორის, <strong className="font-semibold text-[#2C332A]">ClimaComfort</strong>-ის მიერ, DiscreteHeat-ის უხილავი ბრიტანული ტექნოლოგიით.</p>
                </div>
              </div>
            </div>
          </motion.div>

          <motion.div 
            initial={{ x: 40, opacity: 0 }}
            whileInView={{ x: 0, opacity: 1 }}
            viewport={{ once: true, margin: "-100px" }}
            transition={{ duration: 1 }}
            className="relative h-[600px] w-full order-1 lg:order-2 rounded-sm overflow-hidden shadow-2xl"
          >
             {/* Realistic cabin reference picture */}
             <img
               src="https://images.unsplash.com/photo-1510798831971-661eb04b3739?q=80&w=2574&auto=format&fit=crop"
               alt="A-Frame Wooden Cabin Nature"
               className="w-full h-full object-cover"
             />
          </motion.div>
        </div>
      </section>

      {/* Projects Showcase */}
      <section id="projects" className="py-24 px-6 lg:px-12 bg-[#FDFBF7]">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h3 className="text-[#4A5D4E] tracking-[0.2em] text-xs uppercase mb-4 font-medium">საცხოვრებელი ზონები</h3>
            <h2 className="text-4xl font-serif text-[#2C332A]">ვრცელი არჩევანი თქვენი უნიკალური ცხოვრებისთვის</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
            
            {/* Project 1 */}
            <motion.div 
              initial={{ y: 30, opacity: 0 }}
              whileInView={{ y: 0, opacity: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8 }}
              className="bg-white p-6 shadow-sm border border-gray-100"
            >
              <div className="h-64 w-full bg-gray-200 mb-6 relative overflow-hidden">
                <img src="https://images.unsplash.com/photo-1449844908441-8829872d2607?q=80&w=2000&auto=format&fit=crop" className="object-cover w-full h-full" alt="Forest Zone" />
              </div>
              <h3 className="text-xl font-bold text-[#2C332A] mb-2 font-serif">ტყის ზონა (Forest Zone)</h3>
              <p className="text-sm font-light text-gray-600 mb-6 h-20">ჩაფლული უძველეს ტყეში, ეს ულტრა-თანამედროვე Barnhouse სტილის კოტეჯები გვთავაზობს აბსოლუტურ სიმშვიდეს.</p>
              <ul className="text-sm space-y-2 mb-6 border-t border-gray-100 pt-4 text-gray-700">
                <li className="flex justify-between"><span>ფართობი:</span> <span className="font-semibold">65 მ²</span></li>
                <li className="flex justify-between"><span>ნაკვეთი:</span> <span className="font-semibold">300-400 მ²</span></li>
                <li className="flex justify-between"><span>სტატუსი:</span> <span className="font-semibold">Gold Club Status</span></li>
              </ul>
              <button className="w-full py-3 bg-[#4A5D4E] text-white text-xs uppercase tracking-widest font-semibold hover:bg-[#2C332A] transition-colors">მეტის ნახვა</button>
            </motion.div>

            {/* Project 2 */}
            <motion.div 
              initial={{ y: 30, opacity: 0 }}
              whileInView={{ y: 0, opacity: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="bg-white p-6 shadow-sm border border-gray-100"
            >
              <div className="h-64 w-full bg-gray-200 mb-6 relative overflow-hidden">
                <img src="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2000&auto=format&fit=crop" className="object-cover w-full h-full" alt="Valley Zone" />
              </div>
              <h3 className="text-xl font-bold text-[#2C332A] mb-2 font-serif">ველის ზონა (Valley Zone)</h3>
              <p className="text-sm font-light text-gray-600 mb-6 h-20">ორ სართულიანი კოტეჯები, შექმნილი ოჯახებისთვის. პანორამული ფანჯრებიდან იშლება წალკის ალპური ველების ულამაზესი ხედი.</p>
              <ul className="text-sm space-y-2 mb-6 border-t border-gray-100 pt-4 text-gray-700">
                <li className="flex justify-between"><span>ფართობი:</span> <span className="font-semibold">120 მ²</span></li>
                <li className="flex justify-between"><span>ნაკვეთი:</span> <span className="font-semibold">400-500 მ²</span></li>
                <li className="flex justify-between"><span>სტატუსი:</span> <span className="font-semibold">Platinum Club Status</span></li>
              </ul>
              <button className="w-full py-3 bg-[#4A5D4E] text-white text-xs uppercase tracking-widest font-semibold hover:bg-[#2C332A] transition-colors">მეტის ნახვა</button>
            </motion.div>

          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-[#2C332A] py-12 text-center text-white/60 text-sm">
        <p>© 2026 Green Canyon Eco Village & Resort. All rights reserved.</p>
        <p className="mt-2 text-xs">Targeting LEED Gold & Green Globe Certification</p>
      </footer>

    </main>
  );
}
