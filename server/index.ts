import express, { Express, Request, Response } from 'express';
import {specs} from './swaggerConfig'; // Update the import statement
import swaggerUi from 'swagger-ui-express';
import fs from 'fs';


const app: Express = express();
const port = 8180;

let rateIndex: number = 0;
let rateValues: number[] = [];

let currencyBalance: number = 0;
let balance: number = 1000;

// Middleware to parse JSON in request body
app.use(express.json());
// Serve Swagger UI
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(specs));

//////////////////////////READING THE RATES FROM TXT FILE////////////////////////////////
// Function to update the rate every 5 seconds
function updateRatePeriodically() {
  setInterval(() => {
    // Read the rates from the file
    readRatesFromFile();

    // Update the global variable with the next rate
    rateIndex = (rateIndex + 1) % rateValues.length;
  }, 5000);
}

// Function to read the rates from the file
function readRatesFromFile() {
  // Read the rates from the file
  const data = fs.readFileSync('Rates.txt', 'utf-8').trim().split('\n');
  rateValues = data.map((rate) => parseFloat(rate));
}

// Function to get the current rate
function getCurrentRate(): number {
  return rateValues[rateIndex];
}
///////////////////////////////END OF READING CURRENT RATE VALUE////////////////////////

/**
 * @swagger
 * /:
 *   get:
 *     description: Main screen, this is for test purposes only.
 *     responses:
 *       200:
 *         description: Successful response
 */
app.get('/', (req: Request, res: Response) => {
  res.redirect("/api-docs")
});

/**
 * @swagger
 * /GetRate:
 *   get:
 *     description: Get Current Exchange Rate of the coin
 *     responses:
 *       200:
 *         description: Successful response
 */
// Get Current Exchange Rate
app.get('/GetRate', (req: Request, res: Response) => {
  res.json({rate : getCurrentRate()});
});

/**
 * @swagger
 * /GetBalance:
 *   get:
 *     description: Get Balance in terms of cash
 *     responses:
 *       200:
 *         description: Successful response
 */
// Get Current Exchange Rate
app.get('/GetBalance', (req: Request, res: Response) => {
  res.json({"Balance" : balance});
});

/**
 * @swagger
 * /GetCurrencyBalance:
 *   get:
 *     description: Get Balance in terms of cash
 *     responses:
 *       200:
 *         description: Successful response
 */
// Get Current Exchange Rate
app.get('/GetCurrencyBalance', (req: Request, res: Response) => {
  res.json({"Currency Balance" : currencyBalance});
});

/**
 * @swagger
 * /Buy:
 *   put:
 *     parameters:
 *       - name: buyAmount
 *         in: body
 *         description: The amount to buy (integer).
 *         required: true
 *         schema:
 *           type: integer
 *           format: int32
 *     description: Buy the coin for given amount and update the coin balance
 *     responses:
 *       200:
 *         description: Successful response
 */
// Buy
app.put('/Buy', (req: Request, res: Response) => {
  // Assuming you send JSON with { "buyAmount": buyAmount, "price": buyPrice } in the request body
  const buyAmount: number = req.body.buyAmount;
  const price: number = getCurrentRate();

  // Check if currencyBalance and balance are initialized
  if (currencyBalance === undefined || balance === undefined) {
    res.status(500).json({ error: 'Server error: Currency balance or total balance not initialized' });
    return;
  }

  if (balance < buyAmount * price) {
    res.status(400).json({ error: 'Not enough balance' });
  } else {
    //
    currencyBalance = currencyBalance + buyAmount;
    balance = balance - (buyAmount * price);
    res.json(req.body)
    /*
    res.json({
      'Bought Amount': buyAmount,
      'Bought Exchange Rate': price,
      'Total Currency Balance': currencyBalance,
      'Total Balance': balance,
    });
    */
  }
});

/**
 * @swagger
 * /Sell:
 *   post:
 *     parameters:
 *       - name: buyAmount
 *         in: body
 *         description: The amount to buy (integer).
 *         required: true
 *         schema:
 *           type: integer
 *           format: int32
 *     description: Buy the coin for given amount and update the coin balance
 *     responses:
 *       200:
 *         description: Successful response
 */
// Sell
app.post('/Sell', (req: Request, res: Response) => {
  // Assuming you send JSON with { "amount": buyAmount, "price": buyPrice } in the request body
  const sellAmount: number = req.body.amount;
  const price: number = getCurrentRate();
  if (currencyBalance < sellAmount){
    res.status(400).json({ error: 'Not enough currency balance' });
  }
  else {
    //
    currencyBalance = currencyBalance - sellAmount;
    balance = balance + (sellAmount * price);
    res.json({
      "Sold Amount" : sellAmount,
      "Sold Exchange Rate" : price,
      "Total Currency Balance" : currencyBalance,
      "Total Balance" : balance
    });
  }
});

app.listen(port, () => {
  console.log(`⚡️[server]: Server is running at http://localhost:${port}`);
  updateRatePeriodically();
});
