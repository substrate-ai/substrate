import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
  } from "@/components/ui/card"
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
  } from "@/components/ui/table"
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectTrigger,
    SelectValue,
  } from "@/components/ui/select"
import { useState } from "react";
import { TimeUnit } from "src/types/enums";

type PricingData = {
  name: string;
  pricePerSeconds?: number;
  priceAwsPerHour: number;
  availability?: string;
}

let pricingData : PricingData[] = [
  {
    name: 'CPU (2 cores, 8GB RAM)',
    priceAwsPerHour: 0.115,
  },
  {
    name: 'NVIDIA T4',
    priceAwsPerHour: 0.736,
  },
  {
    name: 'NVIDIA A10G',
    priceAwsPerHour: 1.515,
  },
]



const abbreviationTimeUnit = {
  hour: 'hr',
  minute: 'min',
  second: 'sec',
}


function computePricePerMinute(pricePerSeconds: number) {
  return (pricePerSeconds * 60).toPrecision(2);
}

function computePricePerHour(pricePerSeconds: number) {
  return (pricePerSeconds * 60 * 60).toPrecision(2);
}

function getPrice(pricePerSeconds: number, timeUnit: TimeUnit) {
  return {
    hour: computePricePerHour(pricePerSeconds),
    minute: computePricePerMinute(pricePerSeconds),
    second: pricePerSeconds,
  }[timeUnit];
}

function computePricePerSeconds(priceAwsPerHour: number) {
  return Number((priceAwsPerHour * 3 / 60 / 60).toPrecision(2));
}


type props = {
  view? : TimeUnit
  hideFooter? : boolean
}

export function PricingTable({view, hideFooter} : props) {
  

  const chosenView = view ? view : TimeUnit.hour

  const [timeUnit, setTimeUnit] = useState<TimeUnit>(chosenView);

  const abbreviation = abbreviationTimeUnit[timeUnit];

  pricingData = pricingData.map((data) => {
    return {
      ...data,
      pricePerSeconds: computePricePerSeconds(data.priceAwsPerHour),
    }
  })

  return (
        // className="w-[500px]"
        <Card >
          <CardHeader>
            <CardTitle>Compute Costs</CardTitle>
            <CardDescription>Pay only for what you use</CardDescription>
            <Select onValueChange={(timeUnit: TimeUnit) => setTimeUnit(timeUnit)}>
              {/* className="w-[180px]" */}
              <SelectTrigger >
                <SelectValue defaultValue="hour" placeholder="price per hour"/>
              </SelectTrigger>
              <SelectContent>
                <SelectGroup>
                  <SelectItem value="hour">price per hour</SelectItem>
                  <SelectItem value="minute">price per minute</SelectItem>
                  <SelectItem value="second">price per second</SelectItem>

                </SelectGroup>
              </SelectContent>
            </Select>

          </CardHeader>
          <CardContent>


            <Table>
              <TableHeader>
                <TableRow className="pointer-events-none">
                  {/* className="w-[100px]" */}
                  <TableHead ></TableHead>
                  <TableHead className="text-right">Price per {timeUnit}</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {pricingData.map((data) => (
                  <TableRow key={data.name}>
                    <TableCell className="font-medium">{data.name}</TableCell>
                    {data.availability ? (
                      <TableCell className="text-right">{data.availability}</TableCell>
                    ) : (
                      <TableCell className="text-right">${getPrice(data.pricePerSeconds!, timeUnit)} / {abbreviation}</TableCell>
                    )}
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
          {hideFooter ? null :
            <CardFooter>
                          

            <div>
              <p className="font-bold text-indigo-500">Paid by the second</p>
            </div>

          </CardFooter>
          
          
          }
          

        </Card>

  )
}

