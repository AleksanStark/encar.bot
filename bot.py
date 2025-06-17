import asyncio
import logging
from dataclasses import dataclass
from typing import Union
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, ScenesManager, SceneRegistry, on
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram.types import InlineKeyboardButton, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from encar import CarapisClient
from datetime import datetime, timezone
import requests


TOKEN = "8070729025:AAHxsH-03byNNtRg7L_kIbwcWq-xfSWQrfs"  


@dataclass
class Car:
    brand: str
    models: dict[str, dict[str, list[str]]]
    years: list[str]
    colors: list[str]

# Add this at the top of your file


COLOR_MAPPING = {
    "Белый": "흰색",
    "Черный": "검정색",
    "Серый": "쥐색",
    "Синий": "청색"
    # Add more mappings as needed
}

BRAND_MAPPING = {
    "Hyundai": "현대",
    "Kia": "기아",
    "Genesis": "제네시스",
    "SsangYong":"KG모빌리티(쌍용)",
    "BMW": "BMW",
    "Mercedes-Benz": "벤츠",
    "Audi":"아우디",
    "Volkswagen": "폭스바겐",
    "Porsche": "포르쉐",
    "Volvo": "볼보",
    "Land Rover": "랜드로버",
    "Toyota":"도요타",
  
}

MODEL_MAPPING = {
    "Palisade":"팰리세이드",
    "Santa Fe":"싼타페",
    "Tucson": "투싼",
    "Sonata":"쏘나타",
    "Avante":"아반떼",
    "Staria":"스타리아",
    "Kona":"코나",
    "K5": "K5",
    "Sorrento":"쏘렌토",
    "Sportage":"스포티지",
    "Carnival":"카니발",
    "Mohave":"모하비",
    "Seltos": "셀토스",
    "Niro":"니로",
    "Ray":"레이",
    "Stinger":"스팅어",
    "G70": "G70",
    "G80": "G80",
    "G90": "G90",
    "GV70": "GV80",
    "Rexton":"렉스턴",
    "Torres":"토레스",
    "Korando":"코란도",
    "Tivoli":"티볼리",
    "X3":"X3",
    "X6":"X6",
    "X7": "X7",
    "Series 5":"5시리즈",
    "Series 7":"7시리즈",
    "Series 3": "3시리즈",
    "M4": "M4",
    "M5": "M5",
    "E-Class":"E-클래스",
    "GLS-Class":"GLS-클래스",
    "GLC-Class":"GLC-클래스",
    "GLE-Class":"GLE-클래스",
    "S-Class":"S-클래스",
    "G-Class": "G-클래스",
    "C-Class": "C-클래스",
    "A4":"A4",
    "A6": "A6",
    "Q5": "Q5",
    "Q7": "Q7",
    "Q8": "Q8",
    "A7":"A7",
    "RSQ8":"RSQ8",
    "Porsche Cayenne": "카이엔",
    "Tiguan":"티구안",
    "Touareg":"투아렉",
    "Alphard":"알파드",
    "Camry":"캠리",
    "RAV4": "RAV4",
    "XC60": "XC60",
    "XC90": "XC90",
    "Land Rover Discovery":"디스커버리",
    "Range Rover": "레인지로버"

}


FUEL_TYPE_MAPPING = {
    "Бензин": "가솔린",
    "Дизель": "디젤",
    "Гибрид": {
        "Бензин + Электро": "가솔린+전기",
        "Бензин + LPG": "가솔린+LPG"

    },
    "Электро": "전기",
    "LPG": "LPG(일반인 구입)"
}

DRIVE_MAPPING = {
    "가솔린": {
        "Бензин 2WD": "가솔린 2WD",
        "Бензин 4WD": "가솔린 4WD"
    },
    "디젤": {
        "Дизель 2WD": "디젤 2WD",
        "Дизель 2WD": "디젤 4WD"
    },
    "Гибрид": {
        "Бензин + Электро 2.5 л": "가솔린+전기 2500cc",
        "Бензин + Электро 2.0 л": "가솔린+전기 2000cc",
        "Бензин + Электро 1.6 л": "가솔린+전기 1600cc",
        "Бензин + LPG 1.5 л": "가솔린+LPG 1500cc"
    },
    "전기": {
        "Электро 2WD": "전기",
        "Электро 4WD": "전기"
    },
}



CARS = [
    Car("Hyundai", {
        "Palisade": {"Palisade 2020 - 2025":{

        "Бензин": ["SE", "SEL", "Limited", "Calligraphy"],            
        "Дизель": ["SE", "SEL", "Limited", "Calligraphy"],
        "Гибрид": ["SE", "SEL", "Limited", "Calligraphy"]}},
        
        "Santa Fe": {"Santa Fe 2020 - 2025": 
        {
                                              
        "Бензин":["SE", "SEL", "XRT", "Limited", "Calligraphy"],

        "Дизель": ["SE", "SEL", "XRT", "Limited", "Calligraphy"],

        "Гибрид":["SE", "SEL", "XRT", "Limited", "Calligraphy"],
        }},

    

        "Tucson": {"Tucson 2020 - 2025": {

        "Бензин":["SE", "SEL", "XRT", "Limited"],

        "Дизель":["SE", "SEL", "XRT", "Limited"],

        "Гибрид":["SE", "SEL", "XRT", "Limited"],

        }},

        "Sonata": {"Sonata 2020 - 2025": {

            "Бензин":["SE", "SEL", "N Line", "Limited"],

             "Гибрид":["SE", "SEL", "N Line", "Limited"],
        }},

        "Avante": {"Avante 2020 - 2025": {

        "Бензин":["Smart", "Modern", "Inspiration"],

        "Гибрид": ["Smart", "Modern", "Inspiration"]

        }},

        "Staria": {"Staria 2020 - 2025": {

        "Бензин":["Tourer", "Lounge", "Cargo"],

        "Дизель": ["Tourer", "Lounge", "Cargo"]
        }},

        "Kona": {"Kona 2020 - 2025": {

        "Бензин":["SE", "SEL", "N Line", "Limited"],

        "Гибрид":["SE", "SEL", "N Line", "Limited"],

        "Электро":["SE", "SEL", "N Line", "Limited"],

        }}
    }, ["2020","2021", "2022", "2023", "2024", "2025" ], ["Белый", "Черный", "Серый", "Синий" ]),



    Car("Kia", {
        "K5": {"К5 2020 - 2025": {

        "Бензин":["LX", "LXS", "GT-Line", "EX", "GT"],

        "Гибрид":["LX", "LXS", "GT-Line", "EX", "GT"],
        }},

        "Sportage": {"Sportage 2020 - 2025": {

        "Бензин":["LX", "EX", "X-Line", "SX", "X-Pro"],

        "Дизель":["LX", "EX", "X-Line", "SX", "X-Pro"],

        "Гибрид":["LX", "EX", "X-Line", "SX", "X-Pro"],
        }},

        "Sorento": {"Sorento 2020 - 2025": {

            "Бензин":["LX", "S", "EX", "SX", "SX Prestige"],

            "Дизель":["LX", "S", "EX", "SX", "SX Prestige"],

            "Гибрид":["LX", "S", "EX", "SX", "SX Prestige"],
                                            
        }},

        "Mohave": {"Mohave 2020 - 2025": {

        "Дизель":["Platinum", "Gravity", "Masters"],

        }},

        "Carnival": {"Carnival 2020 - 2025": {

            "Бензин":["LX", "EX", "SX", "SX Prestige"],

            "Дизель":["LX", "EX", "SX", "SX Prestige"],
        }},

        "Seltos": {"Seltos 2020 - 2025": {
            "Бензин":["LX", "S", "EX", "SX"],
            "Дизель":["LX", "S", "EX", "SX"],
        }},

        "Niro": {"Niro 2020 - 2025": {
            "Гибрид":["Trendy", "Prestige", "Noblesse", "Signature", "Earth"],
            "электро":["Trendy", "Prestige", "Noblesse", "Signature", "Earth"]
        }},

        "Stinger": {"Stinger 2020 - 2023": {
            "Бензин":["GT-Line", "GT", "GT1", "GT2"]
        }},

        "Ray": {"Ray 2020 - 2025": {
            "Бензин":["Standard", "Prestige", "Van"],
            "электро":["Standard", "Prestige", "Van"],
        }}

    }, ["2020","2021", "2022", "2023", "2024", "2025" ], ["Белый", "Черный", "Серый", "Синий" ]),
    
    Car("Genesis", {
        "G70": {"G70 2020 - 2025": {
            "Бензин":["Standard", "Sport", "Sport Prestige"]
            }}, 
        "G80": {"G80 2020 - 2025":{
            "Бензин":["2.5T", "3.5T Sport", "Prestige"],
            "электро":["2.5T", "3.5T Sport", "Prestige"],
            }}, 
        "G90": {"G90 2020 - 2025": {
            "Бензин":["3.5T", "Prestige"]
            }},
        "GV70": {"GV70 2020 - 2025": {
            "Бензин":["2.5T", "3.5T Sport", "Prestige"],
            "электро":["2.5T", "3.5T Sport", "Prestige"],
            }},
        "GV80":{"GV80 2020 - 2025": {
            "Бензин":["2.5T", "3.5T", "Advanced", "Prestige"],
            "Дизель":["2.5T", "3.5T", "Advanced", "Prestige"]
                                     }}
        },
        ["2020","2021", "2022", "2023", "2024", "2025" ], ["Белый", "Черный", "Серый", "Синий" ]
    ),

    Car("SsangYong", {
        "Torres": {"Torres 2020 - 2025": {
            "Бензин":["T5", "T7", "T9"], 
            "электро":["T5", "T7", "T9"]
            }},
        "Rexton": {"Rexton 2020 - 2025": {
            "Дизель":["ELX", "Ultimate", "Ventura"]
            }},
        "Korando": {"Korando 2020 - 2025":{  
            "Бензин":["ELX", "Ultimate", "Ventura"],
            "Дизель":["ELX", "Ultimate", "Ventura"],
            "электро":["ELX", "Ultimate", "Ventura"]
            }},

        "Tivoli": {"Tivoli 2020 - 2025": {
            "Бензин":["EX", "ELX", "Ventura"],
            "Дизель":["EX", "ELX", "Ventura"],
            }},

        "Rexton Sports":{"Rexton Sports 2020 - 2025":{
            "Дизель":["Adventure", "Prestige", "Pro"]
            }},
    }, ["2020","2021", "2022", "2023", "2024", "2025" ], ["Белый", "Черный", "Серый", "Синий" ]),

    Car("BMW", {
        "X3":{"X3 (G01) 2020 - 2025": {
            "Бензин":["xDrive30i", "M40i", "xDrive30e"],
            "Дизель":["xDrive30i", "M40i", "xDrive30e"],
            "Гибрид":["xDrive30i", "M40i", "xDrive30e"],},
        },
        "X5":{"X5 (G05) 2020 - 2025": {
        "Бензин":["xDrive40i", "xDrive45e", "M50i"],
        "Дизель":["xDrive40i", "xDrive45e", "M50i"],
        "Гибрид":["xDrive40i", "xDrive45e", "M50i"],
        }},
        "X6": {"X6 (G06) 2020 - 2025": {
            "Бензин":["xDrive40i", "M50i"],
            "Дизель":["xDrive40i", "M50i"],
            "Гибрид":["xDrive40i", "M50i"],
            
        }},
        "X7": {"X7 (G07) 2020 - 2025": {
            "Бензин":["xDrive40i", "M60i", "ALPINA XB7"],
            "Дизель":["xDrive40i", "M60i", "ALPINA XB7"],
            "Гибрид":["xDrive40i", "M60i", "ALPINA XB7"],

        }},
        "5 Series": {"5 Series 2020 - 2025": {
            "Бензин":["530i", "540i", "M550i"],
            "Дизель":["530i", "540i", "M550i"],
            "Гибрид":["530i", "540i", "M550i"],

        }},
        "7 Series": {"7 Series 2020 - 2025": {
            "Бензин":["740i", "760i", "i7"],
            "Дизель":["740i", "760i", "i7"],
            "Гибрид":["740i", "760i", "i7"],

        }},
        "3 Series": {"3 Series 2020 - 2025": {
            "Бензин":["330i", "M340i"],
            "Дизель":["330i", "M340i"],
            "Гибрид":["330i", "M340i"]

        }},
        "M4": {"M4 2020 - 2025": {
            "Бензин":["Base", "Competition"]
        }},
        "M5": {"M5 2020 - 2025": {
            "Бензин":["Base", "Competition", "CS"]
        }}
    }, ["2020","2021", "2022", "2023", "2024", "2025" ], ["Белый", "Черный", "Серый", "Синий" ]),
    Car("Mercedes-Benz", {
        "E-Class": {"E-Class 2020 - 2025": {

            "Бензин":["E350", "E450", "AMG E53", "AMG E63"],
            "Дизель":["E350", "E450", "AMG E53", "AMG E63"],
            "Гибрид":["E350", "E450", "AMG E53", "AMG E63"],
        }},
        "GLC-Class":{"GLC 2020 - 2025": {
            "Бензин":["GLC 300", "GLC 43 AMG", "GLC 63 AMG"],
            "Дизель":["GLC 300", "GLC 43 AMG", "GLC 63 AMG"],
            "Гибрид":["GLC 300", "GLC 43 AMG", "GLC 63 AMG"],
        }},
        "GLE-Class": {"GLE 2020 - 2025": {
            "Бензин":["GLE 350", "GLE 450", "AMG GLE 53", "AMG GLE 63"],
            "Дизель":["GLE 350", "GLE 450", "AMG GLE 53", "AMG GLE 63"],
            "Гибрид":["GLE 350", "GLE 450", "AMG GLE 53", "AMG GLE 63"],
        }},
        "GLS-Class": {"GLS 2020 - 2025": {
            "Бензин":["GLS 450", "GLS 580", "AMG GLS 63"],
            "Дизель":["GLS 450", "GLS 580", "AMG GLS 63"],
            "Гибрид":["GLS 450", "GLS 580", "AMG GLS 63"],
        }},
        "S-Class": {"S-Class 2020 - 2025": {
            "Бензин":["S 500", "S 580", "Maybach"],
            "Дизель":["S 500", "S 580", "Maybach"],
            "Гибрид":["S 500", "S 580", "Maybach"],

        }},

        "G-Class":{"G 2020 - 2025":{
            "Бензин":["G 550", "AMG G 63"],
            "Дизель":["G 550", "AMG G 63"],
        }},
        "C-Class":{"C-Class 2020 - 2025": {
            "Бензин":["C 300", "AMG C 43", "AMG C 63"],
            "Дизель":["C 300", "AMG C 43", "AMG C 63"],
            "Гибрид":["C 300", "AMG C 43", "AMG C 63"],
        }},
    }, ["2020","2021", "2022", "2023", "2024", "2025" ], ["Белый", "Черный", "Серый", "Синий" ]),

    Car("Audi", {
        "A4":{"A4 2020 - 2025": {
            "Бензин":["Premium", "Premium Plus", "Prestige"],
            "Дизель":["Premium", "Premium Plus", "Prestige"],
            "Гибрид":["Premium", "Premium Plus", "Prestige"],
        }},
        "A6": {"A6 2020 - 2025": {
            "Бензин":["Premium", "Premium Plus", "Prestige"],
            "Дизель":["Premium", "Premium Plus", "Prestige"],
            "Гибрид":["Premium", "Premium Plus", "Prestige"],
        }},
        "Q5": {"Q5 2020 - 2025": {
            "Бензин":["Premium", "Premium Plus", "Prestige"],
            "Дизель":["Premium", "Premium Plus", "Prestige"],
            "Гибрид":["Premium", "Premium Plus", "Prestige"],

        }},
        "Q7": {"Q7 2020 - 2025": {
            "Бензин":["Premium", "Premium Plus", "Prestige"],
            "Дизель":["Premium", "Premium Plus", "Prestige"],
            "Гибрид":["Premium", "Premium Plus", "Prestige"],
        }}, 
        "Q8": {"Q8 2020 - 2025": {
            "Бензин":["Premium", "Premium Plus", "Prestige"],
            "Гибрид":["Premium", "Premium Plus", "Prestige"],
        }},

        "A7": {"A7 2020 - 2025": {
            "Бензин":["Premium", "Premium Plus", "Prestige"],
            "Дизель":["Premium", "Premium Plus", "Prestige"],
            "Гибрид":["Premium", "Premium Plus", "Prestige"],
        }},
        "RSQ8": {"RSQ8 2020 - 2025": {
            "Бензин":["Base", "Carbon Black", "Prestige"],
        }}
    }, ["2020","2021", "2022", "2023", "2024", "2025" ],  ["Белый", "Черный", "Серый", "Синий" ]),
    Car("Volkswagen", {
        "Tiguan": {"Tiguan 2020 - 2025": {
            "Бензин":["S", "SE", "SEL", "R-Line"],
            "Дизель":["S", "SE", "SEL", "R-Line"],
          
        }},
        "Touareg": {"Touareg 2020 - 2025": {
            "Бензин": ["Base", "R-Line", "Elegance"],
            "Дизель": ["Base", "R-Line", "Elegance"],
            "Гибрид": ["Base", "R-Line", "Elegance"],
            
        }},
    }, ["2020","2021", "2022", "2023", "2024", "2025" ], ["Белый", "Черный", "Серый", "Синий" ]),

    Car("Porsche", {
         "Porsche Cayenne": {"Porsche Cayenne 2020 - 2025": {
            "Бензин":["Base", "S", "Turbo", "GTS", "E-Hybrid"],
            "Гибрид":["Base", "S", "Turbo", "GTS", "E-Hybrid"],
            
        }},
    }, ["2020","2021", "2022", "2023", "2024", "2025" ], ["Белый", "Черный", "Серый", "Синий" ]),

    Car("Volvo", {
         "XC60": {"Volvo XC60  2020 - 2025":{
            "Бензин":["Momentum", "Inscription", "R-Design", "Ultimate"],
            "Дизель":["Momentum", "Inscription", "R-Design", "Ultimate"],
         }},
        "XC90": {"Volvo XC90 2020 - 2025":{
            "Бензин":["Momentum", "Inscription", "R-Design", "Ultimate"],
            "Дизель":["Momentum", "Inscription", "R-Design", "Ultimate"],
         }},

    },["2020","2021", "2022", "2023", "2024", "2025" ], ["Белый", "Черный", "Серый", "Синий" ]),


    Car("Land Rover", {

     "Land Rover Discovery": 
        {
            "Land Rover Discovery 2020 - 2025": {
            "Бензин":["SE", "HSE", "Autobiography", "First Edition"],
            "Дизель":["SE", "HSE", "Autobiography", "First Edition"],
            "Гибрид":["SE", "HSE", "Autobiography", "First Edition"],
        },
        
        },
    "Range Rover": {
              "Range Rover 2020 - 2025":{"Бензин":["SE", "HSE", "Autobiography", "First Edition"],
            "Дизель":["SE", "HSE", "Autobiography", "First Edition"],
            "Гибрид":["SE", "HSE", "Autobiography", "First Edition"],}
         }

    },["2020","2021", "2022", "2023", "2024", "2025" ], ["Белый", "Черный", "Серый", "Синий" ]),

    Car("Toyota", {
        "Alphard": {"Alphard 2020 - 2025": {
            "Бензин":["Executive Lounge", "G", "X"],
            "Гибрид":["Executive Lounge", "G", "X"],
        }},
        "Camry": {"Camry 2020 - 2025":  {
            "Бензин":["LE", "SE", "XSE", "XLE"],
            "Гибрид":["LE", "SE", "XSE", "XLE"],
            }},
        "RAV4": {"RAV4 2020 - 2025": {
            "Бензин":["LE", "XLE", "Adventure", "TRD Off-Road", "Limited"],
            "Гибрид":["LE", "XLE", "Adventure", "TRD Off-Road", "Limited"],
            }}
    }, ["2020","2021", "2022", "2023", "2024", "2025" ], ["Белый", "Черный", "Серый", "Синий" ])   
]



async def repeat_car_request(callback: CallbackQuery, api_data: dict):
    while True:
        try:
            response = requests.post("https://encarparser-production.up.railway.app/send_car_info", json=api_data)
            response.raise_for_status()
            result = response.json()
            car_id = result.get("id", "")

            print(f"[DEBUG] Car ID: {car_id}")

            if car_id:
                await callback.message.answer("🚗 Автомобиль найден!")
                await callback.message.edit_text(f"https://fem.encar.com/cars/detail/${car_id}")
                break  # Остановить цикл
            else:
                await callback.message.answer("⏳ Авто не найдено. Попробуем через час...")
                await asyncio.sleep(3600)  # Ждать 1 час
        except Exception as e:
            print(f"[ERROR] {e}")
            await asyncio.sleep(3600)


def create_keyboard(options: list[str], prefix: str, back_callback: str = None):
    keyboard = InlineKeyboardBuilder()
    for opt in options:
        keyboard.add(InlineKeyboardButton(text=opt, callback_data=f"{prefix}:{opt}"))
    if back_callback:
        keyboard.add(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"back:{back_callback}"))
    return keyboard.adjust(2).as_markup()


def create_multiple_choice_keyboard(selected: list[str], items: list[str], prefix: str, back_callback: str = None):
    keyboard = InlineKeyboardBuilder()
    for item in items:
        if item in selected:
            text = f"✔️ {item}"
        else:
            text = item
        keyboard.add(InlineKeyboardButton(
            text=text,
            callback_data=f"{prefix}:{item}"
        ))
    # Add Done button
    keyboard.add(InlineKeyboardButton(text="✅ Готово", callback_data=f"{prefix}:done"))
    if back_callback:
        keyboard.add(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"back:{back_callback}"))
    return keyboard.adjust(2).as_markup(resize_keyboard=True)


class CarSelectionScene(Scene, state="car_selection"):
    @on.message.enter()
    async def enter(self, message: Message, state: FSMContext, step: int | None = 0):
        brands = [car.brand for car in CARS]
        await message.answer("Выберите марку:", reply_markup=create_keyboard(brands, "brand"))
        
    @on.callback_query(F.data.startswith("brand:"))
    async def select_brand(self, callback: CallbackQuery, state: FSMContext):
        brand = callback.data.split(":", 1)[1]
        await state.update_data(brand=brand)
        car = next(c for c in CARS if c.brand == brand)
        models = list(car.models.keys())
        await callback.message.edit_text("Выберите модель:", reply_markup=create_keyboard(models, "model", back_callback="brand"))
        await self.wizard.retake(step=1)

    # @on.callback_query(F.data.startswith("model:"))
    # async def select_model(self, callback: CallbackQuery, state: FSMContext):
    #     model = callback.data.split(":", 1)[1]
    #     await state.update_data(model=model)
    #     fuels = [f for f in FUEL_TYPE_MAPPING.keys()]
    #     await callback.message.edit_text("Выберите топливо:", reply_markup=create_keyboard(fuels, "fuel", back_callback="model"))
    @on.callback_query(F.data.startswith("model:"))
    async def select_model(self, callback: CallbackQuery, state: FSMContext):
        model = callback.data.split(":", 1)[1]
        await state.update_data(model=model)
        fuels = [f for f in FUEL_TYPE_MAPPING.keys() if f != "Гибрид"] + ["Гибрид"]
        await callback.message.edit_text("Выберите топливо:", reply_markup=create_keyboard(fuels, "fuel", back_callback="model"))


    @on.callback_query(F.data.startswith("fuel:"))
    async def select_fuel(self, callback: CallbackQuery, state: FSMContext):
        fuel = callback.data.split(":", 1)[1]

        if fuel == "Гибрид":
            types_of_hybrid = list(FUEL_TYPE_MAPPING["Гибрид"].keys())
            await callback.message.edit_text(
                "Выберите тип гибрида:",
                reply_markup=create_keyboard(types_of_hybrid, "hybrid", back_callback="fuel")
            )
            return

        # Сохраняем сразу на корейском
        korean_fuel = FUEL_TYPE_MAPPING.get(fuel)
        await state.update_data(fuel=korean_fuel)

        data = await state.get_data()
        brand = data["brand"]
        model = data["model"]
        car = next(c for c in CARS if c.brand == brand)
        generations = list(car.models[model].keys())

        await callback.message.edit_text(
            "Выберите поколение:",
            reply_markup=create_keyboard(generations, "generations", back_callback="fuel")
        )

    @on.callback_query(F.data.startswith("hybrid:"))
    async def select_hybrid_type(self, callback: CallbackQuery, state: FSMContext):
        hybrid_type = callback.data.split(":", 1)[1]
        korean_fuel = FUEL_TYPE_MAPPING["Гибрид"].get(hybrid_type)

        await state.update_data(fuel=korean_fuel)
        await state.update_data(hybrid_drive=hybrid_type)

        data = await state.get_data()
        brand = data["brand"]
        model = data["model"]
        car = next(c for c in CARS if c.brand == brand)
        generations = list(car.models[model].keys())

        await callback.message.edit_text(
            "Выберите поколение:",
            reply_markup=create_keyboard(generations, "generations", back_callback="fuel")
        )

    @on.callback_query(F.data.startswith("generations:"))
    async def select_trim(self, callback: CallbackQuery, state: FSMContext):
        generation = callback.data.split(":", 1)[1]
        await state.update_data(generation=generation)
        data = await state.get_data()
        fuel_type = data["fuel"]
     
        
        # Получаем доступные варианты привода для выбранного типа топлива
        if "+" in fuel_type:
            available_drives = DRIVE_MAPPING["Гибрид"]  
        else: 
            available_drives = DRIVE_MAPPING[fuel_type]
                
        # Создаем кнопки с человеко-читаемыми названиями
        drive_buttons = [d for d in available_drives.keys()]
        
        await callback.message.edit_text(
            f"Выберите привод:",
            reply_markup=create_keyboard(
                drive_buttons,
                "drive", 
                back_callback="generations"
            )
        )
        
        # Сохраняем маппинг для последующего использования в бэкенде


    @on.callback_query(F.data.startswith("drive:"))
    async def select_mile(self, callback: CallbackQuery, state: FSMContext):
        drive = callback.data.split(":", 1)[1]
        data =  await state.get_data()
        fuel_key = data["fuel"].split("+")[0] if "+" in data["fuel"] else data["fuel"]
       

        korean_drive = DRIVE_MAPPING.get(fuel_key, {}).get(drive)
        await state.update_data(drive=drive, korean_drive=korean_drive)
        mileages = ["до 20000", "до 40000", "до 60000", "до 80000", "до 100000", "до 120000", "до 140000", "до 160000", "до 180000", "до 200000"]

        await callback.message.edit_text(f"Выберите пробег:", reply_markup=create_keyboard(mileages, "mileage", back_callback="trim"))
        
    
    @on.callback_query(F.data.startswith("mileage:"))
    async def select_year(self, callback: CallbackQuery, state: FSMContext):
            mileage = callback.data.split(":", 1)[1]
            await state.update_data(mileage=mileage)
            data = await state.get_data()
            selected_years = data.get("selected_years", [])
            car = next(c for c in CARS)  # Get any car to access years list
            
            await callback.message.edit_text(
                f"Выберите год выпуска (можно несколько):",
                reply_markup=create_multiple_choice_keyboard(
                    selected_years, 
                    car.years, 
                    "year", 
                    back_callback="mileage"
                )
            )

    @on.callback_query(F.data.startswith("year:"))
    async def handle_year_selection(self, callback: CallbackQuery, state: FSMContext):
        selected_year = callback.data.split(":", 1)[1]
        data = await state.get_data()
        selected_years = data.get("selected_years", [])
        
        if selected_year == "done":
            if not selected_years:
                await callback.answer("Выберите хотя бы один год!")
                return
            await state.update_data(years=selected_years)
            car = next(c for c in CARS)  # Get any car to access colors list
            await callback.message.edit_text(
                "Выберите цвет:",
                reply_markup=create_keyboard(car.colors, "color", back_callback="year")
            )
            return
        
        if selected_year in selected_years:
            selected_years.remove(selected_year)
        else:
            selected_years.append(selected_year)
        
        await state.update_data(selected_years=selected_years)
        
        # Update the keyboard with new selection
        car = next(c for c in CARS)
        await callback.message.edit_reply_markup(
            reply_markup=create_multiple_choice_keyboard(
                selected_years,
                car.years,
                "year",
                back_callback="mileage"
            )
        )
        await callback.answer()
    @on.callback_query(F.data.startswith("color:"))
    async def select_color(self, callback: CallbackQuery, state: FSMContext):
        color = callback.data.split(":", 1)[1]
        await state.update_data(
            color=color,
            search_stopped=False  # Reset stop flag
        )
        data = await state.get_data()
        
        # Prepare API request
        api_data = {
    "min_year": min(data["years"]),
    "max_year": max(data["years"]),
    "fuel_type": data["fuel"],
    "brand": BRAND_MAPPING.get(data["brand"], "Hyundai"),
    "model": MODEL_MAPPING.get(data["model"]),
    "color": COLOR_MAPPING.get(data["color"]),
    "max_mileage": data["mileage"].replace("до ", "").replace("000", "000"),
    "drive": data.get("korean_drive")

}

        print(api_data["brand"])
        print(api_data["fuel_type"])
        print(api_data["drive"])
        print(api_data["color"])
        await callback.message.edit_text("🔍 Начинаем поиск автомобилей... (для поиска других машин используйте команду /start)")

        asyncio.create_task(repeat_car_request(callback, api_data))
        


    @on.callback_query(F.data.startswith("back:"))
    async def go_back(self, callback: CallbackQuery, state: FSMContext):
            back = callback.data.split(":", 1)[1]
            data = await state.get_data()
            brand = data.get("brand")
            model = data.get("model")
            
            car = next(c for c in CARS if c.brand == brand)
            
            if back == "brand":
                brands = [car.brand for car in CARS]
                await callback.message.edit_text(
                    "Выберите марку:",
                    reply_markup=create_keyboard(brands, "brand")
                )
            elif back == "model":
                models = list(car.models.keys())
                await callback.message.edit_text(
                    "Выберите модель:",
                    reply_markup=create_keyboard(models, "model", back_callback="brand")
                )
            elif back == "fuel":
                # Get the first generation's fuel types (keys)
                fuels = [f for f in FUEL_TYPE_MAPPING.keys() if f != "Гибрид"] + ["Гибрид"]
                await callback.message.edit_text(
                    "Выберите топливо:",
                    reply_markup=create_keyboard(fuels, "fuel", back_callback="model")
                )
            elif back == "generations":
                generations = list(car.models[model].keys())
                await callback.message.edit_text(
                    "Выберите поколение:",
                    reply_markup=create_keyboard(generations, "generations", back_callback="fuel")
                )
            elif back == "trim":
                trims = list({
                trim
                for generation_data in car.models[model].values()
                for trim_list in generation_data.values()
                for trim in trim_list})
                await callback.message.edit_text(
                    "Выберите комплектацию:",
                    reply_markup=create_keyboard(trims, "trim", back_callback="generations"))
            elif back == "year":
                mileages = ["до 20000", "до 40000", "до 60000", "до 80000", "до 100000", 
                        "до 120000", "до 140000", "до 160000", "до 180000", "до 200000"]
                await callback.message.edit_text(
                    "Выберите пробег:",
                    reply_markup=create_keyboard(mileages, "mileage", back_callback="trim")
                )
    
car_router = Router(name=__name__)
car_router.message.register(CarSelectionScene.as_handler(), Command("start"))

def create_dispatcher():
    dp = Dispatcher(events_isolation=SimpleEventIsolation())
    dp.include_router(car_router)

    scene_registry = SceneRegistry(dp)
    scene_registry.add(CarSelectionScene)

    return dp

async def main():
    dp = create_dispatcher()
    bot = Bot(token=TOKEN)
    
    try:
        await dp.start_polling(bot)
    finally:
        # Clean up on shutdown
        await bot.session.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,  format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",)

    asyncio.run(main())

