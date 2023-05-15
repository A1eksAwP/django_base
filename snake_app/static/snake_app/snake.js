const GAME_STATUS_STARTED = 'started';
const GAME_STATUS_PAUSED  = 'paused';
const GAME_STATUS_STOPPED = 'stopped';

const SNAKE_DIRECTION_UP = 'up';
const SNAKE_DIRECTION_DOWN = 'down';
const SNAKE_DIRECTION_LEFT = 'left';
const SNAKE_DIRECTION_RIGHT = 'right';
let getUserDelay = [250, 100, 60, 40]
let timer;
let lastEvent = {keyCode: 39};
let diff = 0;
const DIFFICULTY = ['easy', 'medium', 'hard', 'hardcore']

/**
 * Объект с настройками конфигурации игры
 */
const config = {
    /**
     * Размер поля.
*/
    size: 16
};

/**
 * Основной объект игры.
 */
const game = {
    /**
     * Функция ищет HTML элемент контейнера игры на странице.
     *
     * @returns {HTMLElement} Возвращает HTML элемент.
     */
    score: 0,
    nowstatus: '',
    getElement() {
        return document.getElementById('game');
    },


    /**
     * Функция выполняет старт игры.
     */
    setDelay() {
        // timer = setInterval(() => this.move(), 150);
        if (game.nowstatus == 'paused' || game.nowstatus == 'stopped' ){
            clearTimeout(timer)
        } else if (game.nowstatus == 'started') {
            timer = setTimeout(function delay() {
                if (game.nowstatus == GAME_STATUS_STARTED){
                console.log('step!');
                game.move();
                timer = setTimeout(delay, getUserDelay[diff])
                }
            }, 0);
        } else clearTimeout(timer)
    },
    start() {
        console.log('Сработала функция START')
        document.getElementById('send_score').style.display = 'none'
        document.getElementsByClassName('restart')[0].innerText = 'Перезапуск'
        document.getElementById('settings').style.display = 'none'
        document.getElementById('hint').innerText = '(Для выбора другого уровня сложности нажми паузу)'
        lastEvent = {keyCode: 39}
        const pauseButton = document.getElementById('button-pause');
        pauseButton.removeEventListener('click', game.continue);
        pauseButton.addEventListener('click', game.pause);
        pauseButton.innerText = 'Пауза'
        game.setGameStatus(GAME_STATUS_STARTED);
        window.addEventListener('keydown', game.move);
        lastEvent.keyCode = ''
        document.querySelectorAll('.cell').forEach((node) => {node.remove()}) //UPD: удаляет предыдущее отредендеренное поле
        board.render();
        snake.parts = [{ top: 0, left: 0 },{ top: 0, left: 1 },{ top: 0, left: 2 },], //UPD: возвращает змейке стандартное положение
        snake.render();
        game.score = 0; //UPD: сбрасываем очки при каждом перезапуске игры
        document.getElementsByClassName('value')[0].innerText = `SCORE: ${game.score}`
        food.items = [{ top: 5, left: 2 },{ top: 12, left: 10 },{ top: 7, left: 14 }], //UPD: возвращает фруктам стандартное положение
        food.render();
        game.continue()
        snake.direction = SNAKE_DIRECTION_RIGHT //UPD: возвращает по умолчанию вправо, так как был баг, если змейка при столкновении двигалась вверх или влево
        document.getElementsByClassName('status')[0].innerText = 'Игра запущена'
        game.setDelay();

    },

    /**
     * Функция выполняет паузу игры.
     */
    continue() {
        console.log('Сработала функция CONTINUE')
        clearTimeout(timer)
        if (game.nowstatus == GAME_STATUS_PAUSED){
            game.setGameStatus(GAME_STATUS_STARTED);
            window.addEventListener('keydown', game.move);
            document.getElementById('settings').style.display = 'none'
            document.getElementById('hint').innerText = '(Для выбора другого уровня сложности нажми паузу)'
            game.setDelay();
            const pauseButton = document.getElementById('button-pause');
            pauseButton.removeEventListener('click', game.continue);
            pauseButton.addEventListener('click', game.pause);
            pauseButton.innerText = 'Пауза'
            console.log('Вы продолжили игру!')
            document.getElementsByClassName('status')[0].innerText = 'Игра запущена'

        }
    },

    pause() {
        console.log('Сработала функция PAUSE')
        if (game.nowstatus == GAME_STATUS_STARTED) {
        game.setGameStatus(GAME_STATUS_PAUSED);
        window.removeEventListener('keydown', game.move);
        document.getElementById('settings').style.display = 'block'
        document.getElementById('hint').innerText = '(Для выбора другого уровня сложности повторно нажми нынешний)'
        const pauseButton = document.getElementById('button-pause');
        pauseButton.removeEventListener('click', game.pause);
        pauseButton.addEventListener('click', game.continue);
        pauseButton.innerText = 'Продолжить'
        console.log('Игра была поставлена пользователем на паузу')
        document.getElementsByClassName('status')[0].innerText = 'Пауза'
        document.querySelectorAll('.board')[0].classList.toggle('pulse')
        setTimeout(board.foodFinded, 260);
        return game.nowstatus = GAME_STATUS_PAUSED
        }
        /* добавить сюда код */
    },

    /**
     * Функция останавливает игру.
     */
    stop() {
        console.log('Сработала функция STOP')
        document.getElementsByClassName('status')[0].innerText = 'Конец игры'
        game.setGameStatus(GAME_STATUS_STOPPED);
        // if (game.nowstatus === GAME_STATUS_STOPPED) {
        clearTimeout(timer)
        // document.querySelectorAll(".buttons-diff>button").forEach((button) => button.removeAttribute("disabled"))
        // document.querySelectorAll(".buttons-diff>button").forEach((button) => button.toggleAttribute("disabled"))
        document.getElementById('settings').style.display = 'none'
        document.getElementById('hint').innerText = '(Для выбора другого уровня сложности нажми паузу)'
        document.getElementById('send_score').style.display = 'block'
        document.getElementById('post_score').value = game.score
        document.getElementById('post_difficulty').value = diff
        window.removeEventListener('keydown', game.move);
        document.querySelectorAll('.snake').forEach((snakes) => {snakes.remove()})
        document.querySelectorAll('.cell').forEach((node) => {node.remove()})
        board.render();
        food.render();
        const pauseButton = document.getElementById('button-pause');
        pauseButton.removeEventListener('click', game.pause.bind(game));
        pauseButton.removeEventListener('click', game.continue.bind(game));

        console.log('Игра окончена!')
        // }
        /* добавить сюда код */
    },

    /**
     * Функция выполняет передвижение змейки по полю.
     *
     * @param event {KeyboardEvent} Событие нажатия на клавишу.
     */
    move(event) {
        // debugger
        if (game.nowstatus == GAME_STATUS_PAUSED) return
        if (event) {

            lastEvent = event;
            return
          } else {
            event = lastEvent;
          }
        let direction = snake.direction;
        /* смотрим на код клавиши и
         * устанавливаем соответсвующее направление движения */
        // debugger
        if (game.nowstatus===GAME_STATUS_STARTED){
            if (event.keyCode){
                switch (event.keyCode) {
                    case 38:
                        direction = SNAKE_DIRECTION_UP;
                        break;
                    case 40:
                        direction = SNAKE_DIRECTION_DOWN;
                        break;
                    case 37:
                        direction = SNAKE_DIRECTION_LEFT;
                        break;
                    case 39:
                        direction = SNAKE_DIRECTION_RIGHT;
                        break;
                    default:
                        return;
                }
            }

        }

        snake.setDirection(direction);
        const nextPosition = snake.getNextPosition();
        /* проверяем совпадает ли следующая позиция с какой-нибудь едой */
        const foundFood = food.foundPosition(nextPosition);

        /* если найден индекс еды (то есть позиция совпадает) */
        if (foundFood !== -1) {
            /* устанавливаем следующую позицию змейки с вторым параметром 'не удалять хвост змейки',
             * змейка съев еду вырастает на одну клетку */
            snake.setPosition(nextPosition, false);
            if (snake.parts.length>config.size/4){ game.score+=25+100*diff} else {game.score+=100}
            if (snake.parts.length>config.size/4*2){ game.score+=50+1000*diff}
            if (snake.parts.length>config.size/4*3){ game.score+=100+1000*diff}
            if (snake.parts.length>config.size/4*4){ game.score+=250+1000*diff}
            if (snake.parts.length>config.size/4*5){ game.score+=500+10000*diff}
            if (snake.parts.length>config.size/4*6){ game.score+=1000+100000*diff}
            if (snake.parts.length>config.size/4*7){ game.score+=10000+100000*diff}
            if (snake.parts.length>config.size/4*8){ game.score+=100000+100000*diff}
            if (snake.parts.length>config.size/4*9){ game.score+=1000000+10000000*diff}
            if (snake.parts.length>config.size/4*10){ game.score+=5000000+10000000*diff}
            document.getElementsByClassName('value')[0].innerText = `SCORE: ${game.score}`
            /* удаляем еду с поля */
            food.removeItem(foundFood);

            /* генерируем новую еду на поле */
            food.generateItem();

            /* перерендериваем еду */
            food.render();

        } else {
            /* если индекс не найден, то просто устанавливаем новую координату для змейки */
            snake.setPosition(nextPosition);
        }

        /* перерендериваем змейку */
        snake.render();
        //!!!!!!!!!!!!!!
        // debugger
        // setInterval(game.move, 1000);
        //!!!!!!!!!!!!!!
    },

    /**
     * Функция устанавливает текущий статус игры,
     * раскрашивая контейнер игры в нужный цвет.
     *
     * @param status {GAME_STATUS_STARTED | GAME_STATUS_PAUSED | GAME_STATUS_STOPPED} Строка представляющая статус.
     */
    setGameStatus(status) {
        const element = game.getElement();

        // обратить внимание, как сделать красивее
        element.classList.remove(GAME_STATUS_STARTED, GAME_STATUS_PAUSED, GAME_STATUS_STOPPED);
        element.classList.add(status);
        game.nowstatus = status
    }
};

/**
 * Объект, представляющий поле, где ползает змейка.
 */
const board = {

    // cells: [
    //     { top: 0, left: 0, className: '' }
    // ],

    /**
     * Функция ищет HTML элемент поля на странице.
     *
     * @returns {HTMLElement} Возвращает HTML элемент.
     */
    getElement() {
        return document.getElementById('board');
    },

    foodFinded(){
        document.querySelectorAll('.board')[0].classList.toggle('pulse')
    },

    /**
     * Функция отрисовывает поле с клетками для игры.
     */
    render() {
        const board = this.getElement();
        // document.querySelectorAll('.cell').forEach((node) => {node.remove()}) //UPD: удаляет предыдущее отредендеренное поле
        /* рисуем на странице 20*20 клеток */
        for (let i = 0; i < config.size**2; i++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');

            /* высчитываем и записываем в data атрибуты
             * координаты от верхней и левой границы */
            cell.dataset.top = Math.trunc(i / config.size);
            cell.dataset.left = i % config.size;

            board.appendChild(cell);
        }
    }
};

/**
 * Объект, представляющий клетку на поле.
 */
const cells = {


    /**
     * Функция ищет HTML элементы клеток на странице.
     *
     * @returns { HTMLCollectionOf.<Element>} Возвращает набор HTML элементов.
     */
    getElements() {
        return document.getElementsByClassName('cell');
    },

    /**
     * Функция задает класс для клетки по заданным координатам.
     *
     * @param coordinates {Array.<{top: number, left: number}>} Массив координат клеток для изменения.
     * @param className {string} Название класса.
     */
    renderItems(coordinates, className) {
        const cells = this.getElements();

        /* для всех клеток на странице удаляем переданный класс */
        for (let cell of cells) {
            cell.classList.remove(className);
        }

        /* для заданных координат ищем клетку и добавляем класс */
        for (let coordinate of coordinates) {
            const cell = document.querySelector(`.cell[data-top='${coordinate.top}'][data-left='${coordinate.left}']`);
            cell.classList.add(className);
        }
    }
};

/**
 * Объект, представляющий змейку.
 */
const snake = {

    /**
     * Текущее направление движение змейки.
     * По умолчанию: направо, потому змейка при старте занимает первые три клетки.
     */
    direction: SNAKE_DIRECTION_RIGHT,

    /**
     * Содержит массив объектов с координатами частей тела змейки.
     * По умолчанию: первые три клетки.
     *
     * NOTE: обратить внимание, как сделать красивее.
     * Поменять порядок координат, сейчас первый элемент массива означает хвост.
     */
    parts: [
        { top: 0, left: 0 },
        { top: 0, left: 1 },
        { top: 0, left: 2 },
    ],

    /**
     * Функция устанавливает направление движения.
     *
     * @param direction {'up' | 'down' | 'left' | 'right'} Направление движения змейки.
     */
    setDirection(direction) {
        /* проверка не пытается ли пользователь пойти в противоположном направлении,
         * например, змейка ползет вправо, а пользователь нажал стрелку влево */
        /* обратить внимание, как сделать красивее и сократить условие */
        if (this.direction === SNAKE_DIRECTION_UP && direction === SNAKE_DIRECTION_DOWN
            || this.direction === SNAKE_DIRECTION_DOWN && direction === SNAKE_DIRECTION_UP
            || this.direction === SNAKE_DIRECTION_LEFT && direction === SNAKE_DIRECTION_RIGHT
            || this.direction === SNAKE_DIRECTION_RIGHT && direction === SNAKE_DIRECTION_LEFT) {
            return;
        }

        this.direction = direction;
    },

    /**
     * Функция считает следующую позицию головы змейки,
     * в зависимости от текущего направления.
     *
     * @returns {{top: number, left: number}} Возвращает объект с координатами.
     */
    getNextPosition() {
        /* получаем позицию головы змейки */
        const position = { ...this.parts[this.parts.length - 1] };

        /* в зависимости от текущего положения
         * высчитываем значение от верхней и левой границы */
        if (game.nowstatus !== GAME_STATUS_STOPPED) {
        switch(this.direction) {
            case SNAKE_DIRECTION_UP:
                position.top -= 1;
                break;
            case SNAKE_DIRECTION_DOWN:
                position.top += 1;
                break;
            case SNAKE_DIRECTION_LEFT:
                position.left -= 1;
                break;
            case SNAKE_DIRECTION_RIGHT:
                position.left += 1;
                break;
        }
        for (part in snake.parts) {
            if (position.top == snake.parts[part].top && position.left == snake.parts[part].left) {
                console.log('Ты врезался сам в себя!')
                clearTimeout(timer)
                game.stop();
                document.getElementsByClassName('status')[0].innerText = 'Ты врезался сам в себя!'
                break
            }
        }
        /* если змейка выходит за верхний или нижний край поля,
         * то изменяем координаты на противоположную сторону, !UPD: закончим игру
         * чтобы змейка выходя за границы возвращалась обратно на поле */
        if (position.top === -1 || position.left === -1 || position.top > config.size - 1 || position.left > config.size - 1) {
            console.log('Ты врезался в стену!')
            // debugger
            clearTimeout(timer)
            game.stop();
            position.top = snake.parts[snake.parts.length-1].top; position.left = snake.parts[snake.parts.length-1].left
            document.getElementsByClassName('status')[0].innerText = 'Ты врезался в стену!'
            return position
        } else {return position;}
        } else {position.top = snake.parts[snake.parts.length-1].top; position.left = snake.parts[snake.parts.length-1].left
        return position}
    },

    /**
     * Функция устанавливает позицию для змейки.
     *
     * @param position {{top: number, left: number}} Координаты новой позиции.
     * @param shift Флаг, указывающий, нужно ли отрезать хвост для змейки.
     */


    setPosition(position, shift = true) {
        /* проверяем флаг, указывающий, нужно ли отрезать хвост для змейки,
         * если флаг положительный, то отрезаем хвост змейки (первый элемент в массиве),
         * чтобы длина змейки не изменилась,
         * если флаг будет отрицательным, то при установки позиции, мы не отрезаем хвост,
         * а значит увеличиваем змейку на одну клетку, это будет означать, что она съела еду */
        if (shift) {
            this.parts.shift();
        }

        /* добавляем новые координаты в конец массива (голова змейки) */
        this.parts.push(position);
    },

    /**
     * Функция отрисовывает змейку на поле.
     */
    render() {
        if (game.nowstatus != GAME_STATUS_STOPPED){
            cells.renderItems(this.parts, 'snake');
            document.querySelectorAll('.snake').forEach((node) => {node.classList.remove('snakebreak')})
        } else {
            cells.renderItems(this.parts, 'snake');
            document.querySelectorAll('.snake').forEach((node) => {node.classList.toggle('snakebreak')})
        }
    }
};

/**
 * Объект, представляющий еду для змейки.
 */
const food = {

    /**
     * Содержит массив объектов с координатами еды на поле.
     */
    items: [
        { top: 4, left: 2 },
        { top: 1, left: 2 },
        { top: 4, left: 3 }
    ],

    /**
     * Функция выполняет поиск переданных координат змейки в массиве с едой.
     *
     * @param snakePosition {{top: number, left: number}} Позиция головы змейки.
     *
     * @returns {number} Возвращает индекс найденного совпадения из массива с едой,
     * если ничего не найдено, то -1.
     */
    foundPosition(snakePosition) {
        /* здесь происходит вызов функции comparerFunction для каждого элемента в массиве,
         * если функция вернет true, то для этого элемента будет возвращен его индекс,
         * если функция ни разу не вернет true, то результатом будет -1 */
        return this.items.findIndex((item) =>
            item.top === snakePosition.top && item.left === snakePosition.left
        );
    },

    /**
     * Функция удаляет один элемент по индексу из массива с едой.
     *
     * @param foundPosition Индекс найденного элемента.
     */
    removeItem(foundPosition) {
        this.items.splice(foundPosition, 1);
    },

    /**
     * Функция генерирует объект с координатами новой еды.
     */
    generateItem() {
        let newItem = {
            top: getRandomNumber(0, config.size - 1),
            left: getRandomNumber(0, config.size - 1)
        };
            for (let i=0; i<snake.parts.length;i++){
            if (newItem.top == snake.parts[i].top && newItem.left == snake.parts[i].left) {
                newItem = {
                top: getRandomNumber(0, config.size - 1),
                left: getRandomNumber(0, config.size - 1)
                }
                i = 0
            }
            }
            for (fruit in food.items) {
                if (newItem.top == food.items[fruit].top && newItem.left == food.items[fruit].left) {
                    return food.generateItem()
                }
            }
        food.items.push(newItem);
    },

    /**
     * Функция отрисовывает еду на поле.
     */
    render() {
        cells.renderItems(this.items, 'food');
        document.querySelectorAll('.board')[0].classList.toggle('pulse')
        setTimeout(board.foodFinded, 260);
    }
};

/**
 * Функция, которая выполняет инициализацию игры.
 */
function init() {
    /* получаем кнопки */
    const restartButton = document.getElementById('button-restart');
    const pauseButton = document.getElementById('button-pause');
    const stopButton = document.getElementById('button-stop');
    const setDiffEasyButton = document.getElementById('button-set-diff-easy');
    const setDiffMediumButton = document.getElementById('button-set-diff-medium');
    const setDiffHardButton = document.getElementById('button-set-diff-hard');
    const setDiffHardcoreButton = document.getElementById('button-set-diff-hardcore');

    /* добавляем обработчики клика на кнопки */
    restartButton.addEventListener('click', game.start.bind(game));
    pauseButton.addEventListener('click', game.pause.bind(game));
    stopButton.addEventListener('click', game.stop.bind(game));

    setDiffEasyButton.addEventListener('click', setUserDifficulty)
    setDiffMediumButton.addEventListener('click', setUserDifficulty)
    setDiffHardButton.addEventListener('click', setUserDifficulty);
    setDiffHardcoreButton.addEventListener('click', setUserDifficulty)

    /* добавляем обработчик при нажатии на любую кнопку на клавиатуре,
     * далее в методе мы будем проверять нужную нам клавишу */
    window.addEventListener('keydown', game.move);
}

/**
 * Функция, генерирующая случайные числа.
 *
 * @param min {number} Нижняя граница генерируемого числа.
 * @param max {number} Верхняя граница генерируемого числа.
 *
 * @returns {number} Возвращает случайное число.
 */
function getRandomNumber(min, max) {
    return Math.trunc(Math.random() * (max - min) + min);
}

function setUserDifficulty(){
    document.querySelectorAll(".buttons>button").forEach((button) => button.toggleAttribute("disabled"));
    diff = DIFFICULTY.indexOf(this.className);
    console.log(`Выбран уровень сложности: ${DIFFICULTY[diff]}`)
    this.toggleAttribute("disabled");
}

window.addEventListener('load', init);