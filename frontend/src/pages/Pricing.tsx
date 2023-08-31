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
   
  const pricingData = [
    {
        name: 'CPU (2 cores, 4GB RAM)',
        pricePerHour: 0.15,
    },
    {
        name: 'NVIDIA T4',
        availability: "COMING SOON",

    },
    {
        name: 'NVIDIA A100',
        availability: "COMING SOON",
    },
]
   
  export default function Pricing() {
    return (
        <div className="flex h-screen">
            <div className="m-auto">
        <Card className="w-[500px]">
            <CardHeader>
            <CardTitle>Compute Costs</CardTitle>
            <CardDescription>Pay only for what you use</CardDescription>

        </CardHeader>
      <CardContent>

        
        <Table>
            <TableHeader>
            <TableRow className="pointer-events-none">
                <TableHead className="w-[100px]"></TableHead>
                <TableHead className="text-right">Price per Hour</TableHead>
            </TableRow>
            </TableHeader>
            <TableBody>
            {pricingData.map((data) => (
                <TableRow key={data.name}>
                <TableCell className="font-medium">{data.name}</TableCell>
                {data.availability ? (
                    <TableCell className="text-right">{data.availability}</TableCell>
                ) : (
                    <TableCell className="text-right">${data.pricePerHour} / hr</TableCell>
                )}
                </TableRow>
            ))}
            </TableBody>
        </Table>
      </CardContent>
      <CardFooter>
        <div>
            <p className="font-bold text-indigo-500">Paid by the minute</p>
        </div>
        
      </CardFooter>

      </Card>
        </div>
        </div>
    )
  }

